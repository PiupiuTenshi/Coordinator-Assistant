from __future__ import annotations

import numpy as np
from seqeval.metrics import f1_score, precision_score, recall_score
from sklearn.metrics import accuracy_score, f1_score as sklearn_f1


def compute_ner_metrics(label_list: list[str]):
    def compute(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=2)

        true_predictions = [
            [label_list[pred] for pred, label in zip(prediction, label_row) if label != -100]
            for prediction, label_row in zip(predictions, labels)
        ]
        true_labels = [
            [label_list[label] for pred, label in zip(prediction, label_row) if label != -100]
            for prediction, label_row in zip(predictions, labels)
        ]

        return {
            "precision": precision_score(true_labels, true_predictions),
            "recall": recall_score(true_labels, true_predictions),
            "f1": f1_score(true_labels, true_predictions),
        }

    return compute


def compute_triage_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "macro_f1": sklearn_f1(labels, predictions, average="macro", zero_division=0),
    }
