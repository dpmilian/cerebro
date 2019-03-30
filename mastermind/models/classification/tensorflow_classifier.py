from ..tensorflow_model import TensorFlowModel


class TensorFlowClassifier(TensorFlowModel):
    """
    """
    def postprocess_predictions(self, predictions, top_k=5):
        """
        :param predictions:
        :return:
        """
        class_scores = predictions[0][0]

        top_k_scores = class_scores.argsort()[-top_k:][::-1]
        print(top_k_scores)
        predicted_classes = self.labels[top_k_scores]

        return predicted_classes
