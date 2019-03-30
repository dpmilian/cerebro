from ..tensorflow_model import TensorFlowModel


class TensorFlowDetector(TensorFlowModel):
    """
    """
    def __init__(
        self, model, labels, min_score=0.5, input_shape=[1, 300, 300, 3]):
        """
        :param model:
        :param labels:
        :param input_shape:
        """
        super().__init__(
            model=model,
            labels=labels,
            input_node="image_tensor",
            output_nodes=[
                "detection_boxes",
                "detection_scores",
                "detection_classes"],
            input_shape=input_shape)

        self.min_score = min_score

    def postprocess_predictions(self, predictions):
        """
        :param predictions:
        :return:
        """
        boxes, scores, classes = predictions

        indices_to_keep = scores[0] > self.min_score

        classes = self.labels[classes.astype(int)]

        return boxes[0, indices_to_keep], classes[0, indices_to_keep]
