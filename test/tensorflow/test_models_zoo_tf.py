import pytest
import numpy as np

from doctr import models
from doctr.models.predictor import OCRPredictor
from doctr.io import Document, DocumentFile
from test_models_detection_tf import test_detectionpredictor, test_rotated_detectionpredictor
from test_models_recognition_tf import test_recognitionpredictor


def test_ocrpredictor(
    mock_pdf, test_detectionpredictor, test_recognitionpredictor, test_rotated_detectionpredictor  # noqa: F811
):

    predictor = OCRPredictor(
        test_detectionpredictor,
        test_recognitionpredictor,
        assume_straight_pages=True,
    )

    r_predictor = OCRPredictor(
        test_rotated_detectionpredictor,
        test_recognitionpredictor,
        assume_straight_pages=False,
    )

    doc = DocumentFile.from_pdf(mock_pdf).as_images()
    out = predictor(doc)
    r_out = r_predictor(doc)

    # Document
    assert isinstance(out, Document)
    assert isinstance(r_out, Document)

    # The input PDF has 8 pages
    assert len(out.pages) == 8
    # Dimension check
    with pytest.raises(ValueError):
        input_page = (255 * np.random.rand(1, 256, 512, 3)).astype(np.uint8)
        _ = predictor([input_page])


@pytest.mark.parametrize(
    "det_arch, reco_arch",
    [
        ["db_resnet50", "crnn_vgg16_bn"],
        ["db_resnet50", "sar_resnet31"],
    ],
)
def test_zoo_models(det_arch, reco_arch):
    # Model
    predictor = models.ocr_predictor(det_arch, reco_arch, pretrained=True)
    # Output checks
    assert isinstance(predictor, OCRPredictor)
