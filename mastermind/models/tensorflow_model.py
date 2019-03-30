import abc

import numpy as np
import tensorflow as tf


class TensorFlowModel(abc.ABC):
    """
    Base class for all perception models.

    A TensorFlowModel takes care of:
        - Loading a TensorFlow graph from a trained model.
        - Setting up a TensorFlow session.
        - Extracting information from the graph.
        - Postprocessing the extracted information.
    """
    def __init__(
        self, model, labels, input_node="input", output_nodes=["output"], input_shape=[1, 128, 128, 3]):
        """
        :param model:
            Path to a frozen TensorFlow model in protobuf format (.pb).
        :param labels:
            Path to a .txt file with one class name per line.
            This labels will be used to map the indices (int) predicted by the model to
            their corresponding class name (string).
        :param input_node:
            Name of the node in the graph that will be used to feed the inputs.
        :param output_nodes:
            List of names of nodes in the graph from wich the predictions will be extracted.
            For classification models this is usually only 1 name but we prefer to force
            the class to work with lists in order to support more complex models
            (i.e object detection, that usually uses 3 output nodes.)
        :param input_shape:
            Expected shape for the inputs.
            This is used for the warm start in self.setup_session() and for assertions in
            self.__call__.
            Althoug a TensorFlow graph could dinamically support different input shapes,
            it's more performant to set a fixed input_shape and let TensorFlow optimize
            the graph for that shape with a warm start.
        """
        self.model = model

        with open(labels) as f:
            self.labels = np.array([x.strip() for x in f.readlines()])

        self.input_node = input_node
        self.output_nodes = output_nodes
        self.input_shape = input_shape
        
        self.load_graph()
        self.setup_session()

    def load_graph(self):
        """ Loads and import a TensorFlow graph from a frozen model.
        """
        self.graph = tf.Graph()

        graph_def = tf.GraphDef()

        with open(self.model, "rb") as f:
            graph_def.ParseFromString(f.read())

        with self.graph.as_default():
            # name="" is used to prevent TensorFlow's default prefix: "import/"
            tf.import_graph_def(graph_def, name='')

        self.input_tensor = self.graph.get_tensor_by_name("{}:0".format(self.input_node))
        self.output_tensors = [
            self.graph.get_tensor_by_name("{}:0".format(x)) for x in self.output_nodes]

    def setup_session(self):
        """ Creates and stores a TensorFlow session with warm start.
        """
        self.session = tf.Session(graph=self.graph)
        
        # Warm start ussing the fixed input sphape.
        self.session.run(
            self.output_tensors,
            {self.input_tensor: np.random.rand(*self.input_shape)})

    def get_predictions(self, image):
        """ Extracts raw predictions from the TensorFlow graph for given image.
        :param image:
            Expected to have self.input_shape
        :return:
        """
        predictions = self.session.run(
            self.output_tensors,
            {self.input_tensor: image})

        return predictions

    @abc.abstractmethod
    def postprocess_predictions(self, predictions):
        pass
    
    def __call__(self, image):
        """ Obtains processed predictions for given image.
        :param image:
            Expected to have self.input_shape
        :return:
        """
        if list(image.shape) != list(self.input_shape):
            raise ValueError("image.shape does not match the expected input_shape")
        return self.postprocess_predictions(self.get_predictions(image))
