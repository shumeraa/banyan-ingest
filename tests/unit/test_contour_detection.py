import os
import cv2
import pytest
import numpy as np
from unittest.mock import patch

# Import the functions from your module
from banyan_extract.processor.evaluate_extraction import evaluate_extraction, _clamp, _expand_and_clip_box

def test_clamp():
    """Test value clamping within bounds."""
    assert _clamp(5, 0, 10) == 5
    assert _clamp(-5, 0, 10) == 0
    assert _clamp(15, 0, 10) == 10

def test_expand_and_clip_box():
    """Test bounding box expansion and boundary clipping."""
    # args: xmin, ymin, xmax, ymax, pad_x, pad_y, w, h
    assert _expand_and_clip_box(10, 10, 20, 20, 5, 5, 100, 100) == (5, 5, 25, 25)
    
    # Test clipping exactly to the image boundaries
    assert _expand_and_clip_box(5, 5, 95, 95, 10, 10, 100, 100) == (0, 0, 99, 99)

@pytest.fixture
def dummy_image_bytes():
    """
    Creates a 100x100 white image with a 50x50 black square in the middle.
    This simulates an image with clear distinct content for OpenCV to detect.
    """
    img = np.full((100, 100, 3), 255, dtype=np.uint8)
    
    # Add a black square in the middle
    img[25:75, 25:75] = 0
    
    # Encode to jpg bytes
    success, buffer = cv2.imencode('.jpg', img)
    assert success, "Failed to encode dummy image"
    return buffer.tobytes()

def test_evaluate_extraction_invalid_image():
    """Test how the function handles unreadable image bytes."""
    should_rerun, missed_pct = evaluate_extraction(
        image_bytes=b"invalid_garbage_bytes", 
        bbox_data=[], 
        temperature=0.5
    )
    assert not should_rerun
    assert missed_pct == 0.0

@patch("banyan_extract.processor.evaluate_extraction.cv2.imdecode")
def test_evaluate_extraction_zero_area(mock_imdecode):
    """Test image with zero area dimensions."""
    # Mock OpenCV decode to return a 0x0 shape
    mock_imdecode.return_value = np.zeros((0, 0, 3), dtype=np.uint8)
    
    should_rerun, missed_pct = evaluate_extraction(
        image_bytes=b"fake_bytes", 
        bbox_data=[], 
        temperature=0.5
    )
    assert not should_rerun
    assert missed_pct == 0.0

def test_evaluate_extraction_good_coverage(dummy_image_bytes):
    """Test an extraction where bounding boxes perfectly cover the content."""
    # Bbox spans from 20% to 80%, fully covering the 25% to 75% black square
    bbox_data = [{"bbox": {"xmin": 0.2, "ymin": 0.2, "xmax": 0.8, "ymax": 0.8}}]
    
    should_rerun, missed_pct = evaluate_extraction(
        image_bytes=dummy_image_bytes, 
        bbox_data=bbox_data, 
        temperature=0.5, 
        input_filename="test.jpg"
    )
    
    assert not should_rerun
    assert missed_pct < 8.0

def test_evaluate_extraction_poor_coverage(dummy_image_bytes):
    """Test an extraction missing all content to trigger a rerun."""
    # Providing empty bbox_data implies the OCR/extraction missed everything
    bbox_data = []
    
    should_rerun, missed_pct = evaluate_extraction(
        image_bytes=dummy_image_bytes, 
        bbox_data=bbox_data, 
        temperature=0.5, 
        input_filename="test.jpg"
    )
    
    # The 50x50 square is 25% of the total 100x100 area.
    # Dilation makes it slightly larger so it falls safely between 8.0 and 85.0
    assert should_rerun
    assert 8.0 < missed_pct < 85.0

def test_evaluate_extraction_missing_bbox_key(dummy_image_bytes):
    """Test data formatted incorrectly without the expected 'bbox' key."""
    bbox_data = [{"wrong_key": {"xmin": 0.2, "ymin": 0.2, "xmax": 0.8, "ymax": 0.8}}]
    
    should_rerun, missed_pct = evaluate_extraction(
        image_bytes=dummy_image_bytes, 
        bbox_data=bbox_data, 
        temperature=0.5, 
        input_filename="test.jpg"
    )
    
    assert should_rerun
    assert 8.0 < missed_pct < 85.0

def test_evaluate_extraction_save_fig(dummy_image_bytes, tmp_path):
    """Test the visualization saving logic using pytest's temporary directory."""
    bbox_data = [{"bbox": {"xmin": 0.2, "ymin": 0.2, "xmax": 0.8, "ymax": 0.8}}]
    out_dir = str(tmp_path / "output")
    
    evaluate_extraction(
        image_bytes=dummy_image_bytes, 
        bbox_data=bbox_data, 
        temperature=0.7, 
        input_filename="test_image.jpg", 
        save_fig=True, 
        output_dir=out_dir
    )
    
    display_out_path = os.path.join(out_dir, "test_image_temp0.7_highlight.png")
    bbox_out_path = os.path.join(out_dir, "test_image_temp0.7_bboxes.png")
    
    assert os.path.exists(display_out_path)
    assert os.path.exists(bbox_out_path)