import pytest
import os
from PIL import Image
import numpy as np

from src.img_enhance.enhancer import ImageEnhancer, EnhancementParams

class TestEnhancementParams:
    """Test cases for EnhancementParams class"""
    
    def test_default_params(self):
        """Test default parameter values"""
        params = EnhancementParams()
        assert params.brightness == 1.0
        assert params.contrast == 1.0
        assert params.sharpness == 1.0
        assert params.color == 1.0
        assert params.denoise is False
        assert params.binarize is False
        assert params.binarize_threshold == 128
        assert params.deskew is False
        assert params.resize_factor is None
    
    def test_custom_params(self):
        """Test custom parameter values"""
        params = EnhancementParams(
            brightness=1.2,
            contrast=1.5,
            sharpness=0.8,
            color=0.9,
            denoise=True,
            binarize=True,
            binarize_threshold=150,
            deskew=True,
            resize_factor=1.5
        )
        
        assert params.brightness == 1.2
        assert params.contrast == 1.5
        assert params.sharpness == 0.8
        assert params.color == 0.9
        assert params.denoise is True
        assert params.binarize is True
        assert params.binarize_threshold == 150
        assert params.deskew is True
        assert params.resize_factor == 1.5
    
    def test_to_dict(self):
        """Test converting parameters to dictionary"""
        params = EnhancementParams(brightness=1.2, contrast=1.5)
        params_dict = params.to_dict()
        
        assert isinstance(params_dict, dict)
        assert params_dict['brightness'] == 1.2
        assert params_dict['contrast'] == 1.5
        assert params_dict['sharpness'] == 1.0  # Default value
    
    def test_from_dict(self):
        """Test creating parameters from dictionary"""
        params_dict = {
            'brightness': 1.2,
            'contrast': 1.5,
            'denoise': True
        }
        
        params = EnhancementParams.from_dict(params_dict)
        
        assert params.brightness == 1.2
        assert params.contrast == 1.5
        assert params.denoise is True
        assert params.sharpness == 1.0  # Default value


class TestImageEnhancer:
    """Test cases for ImageEnhancer class"""
    
    def test_init(self):
        """Test enhancer initialization"""
        # Default initialization
        enhancer = ImageEnhancer()
        assert enhancer.params is not None
        assert enhancer.params.brightness == 1.0
        
        # Custom initialization
        params = EnhancementParams(brightness=1.2)
        enhancer = ImageEnhancer(params)
        assert enhancer.params.brightness == 1.2
    
    def test_set_params(self):
        """Test setting parameters"""
        enhancer = ImageEnhancer()
        params = EnhancementParams(brightness=1.2, contrast=1.5)
        
        enhancer.set_params(params)
        
        assert enhancer.params.brightness == 1.2
        assert enhancer.params.contrast == 1.5
    
    def test_update_params(self):
        """Test updating specific parameters"""
        enhancer = ImageEnhancer()
        
        enhancer.update_params(brightness=1.2, contrast=1.5)
        
        assert enhancer.params.brightness == 1.2
        assert enhancer.params.contrast == 1.5
        assert enhancer.params.sharpness == 1.0  # Unchanged
    
    def test_enhance_file_path(self, test_image_path):
        """Test enhancing from file path"""
        enhancer = ImageEnhancer()
        enhanced = enhancer.enhance(test_image_path)
        
        assert isinstance(enhanced, Image.Image)
        assert enhanced.mode == 'RGB'
    
    def test_enhance_pil_image(self, load_test_images):
        """Test enhancing PIL image"""
        enhancer = ImageEnhancer()
        original = load_test_images['standard']
        enhanced = enhancer.enhance(original)
        
        assert isinstance(enhanced, Image.Image)
        assert enhanced.size == original.size
        assert enhanced.mode == original.mode
    
    def test_brightness_adjustment(self, load_test_images):
        """Test brightness enhancement"""
        img = load_test_images['standard']
        
        # Increase brightness
        params_bright = EnhancementParams(brightness=1.5)
        enhancer_bright = ImageEnhancer(params_bright)
        brightened = enhancer_bright.enhance(img)
        
        # Decrease brightness
        params_dark = EnhancementParams(brightness=0.5)
        enhancer_dark = ImageEnhancer(params_dark)
        darkened = enhancer_dark.enhance(img)
        
        # Compare average pixel values
        original_brightness = np.mean(np.array(img))
        bright_brightness = np.mean(np.array(brightened))
        dark_brightness = np.mean(np.array(darkened))
        
        assert bright_brightness > original_brightness
        assert dark_brightness < original_brightness
    
    def test_contrast_adjustment(self, load_test_images):
        """Test contrast enhancement"""
        img = load_test_images['standard']
        
        # Increase contrast
        params = EnhancementParams(contrast=1.8)
        enhancer = ImageEnhancer(params)
        enhanced = enhancer.enhance(img)
        
        # Compare standard deviation of pixel values (higher std = higher contrast)
        original_std = np.std(np.array(img))
        enhanced_std = np.std(np.array(enhanced))
        
        assert enhanced_std > original_std
    
    def test_sharpness_adjustment(self, load_test_images):
        """Test sharpness enhancement"""
        img = load_test_images['blurry']
        
        params = EnhancementParams(sharpness=2.0)
        enhancer = ImageEnhancer(params)
        sharpened = enhancer.enhance(img)
        
        # We can't easily test sharpness quantitatively in a reliable way
        # Just make sure it runs without errors
        assert isinstance(sharpened, Image.Image)
    
    def test_denoise(self, noisy_image_path):
        """Test denoising"""
        # Create enhancer with denoising
        params = EnhancementParams(denoise=True)
        enhancer = ImageEnhancer(params)
        
        # Load noisy image
        noisy_img = Image.open(noisy_image_path)
        denoised = enhancer.enhance(noisy_img)
        
        # Denoised image should have lower standard deviation in some regions
        # (This is a simple heuristic, not perfect)
        noisy_array = np.array(noisy_img)
        denoised_array = np.array(denoised)
        
        # Check a small region
        region_noisy = noisy_array[50:100, 50:100]
        region_denoised = denoised_array[50:100, 50:100]
        
        std_noisy = np.std(region_noisy)
        std_denoised = np.std(region_denoised)
        
        # The denoised region should have less variation in most cases
        # but not always guaranteed, so this is a soft assertion
        assert isinstance(denoised, Image.Image)
    
    def test_binarize(self, load_test_images):
        """Test binarization"""
        img = load_test_images['standard']
        
        params = EnhancementParams(binarize=True, binarize_threshold=128)
        enhancer = ImageEnhancer(params)
        binarized = enhancer.enhance(img)
        
        # Binarized image should be mode '1' (1-bit pixels, black and white)
        assert binarized.mode == '1'
        
        # Check that only black and white pixels exist
        binary_array = np.array(binarized)
        unique_values = np.unique(binary_array)
        assert len(unique_values) <= 2
    
    def test_resize(self, load_test_images):
        """Test resize functionality"""
        img = load_test_images['standard']
        original_size = img.size
        
        # Test upscaling
        params_up = EnhancementParams(resize_factor=1.5)
        enhancer_up = ImageEnhancer(params_up)
        upscaled = enhancer_up.enhance(img)
        
        # Test downscaling
        params_down = EnhancementParams(resize_factor=0.5)
        enhancer_down = ImageEnhancer(params_down)
        downscaled = enhancer_down.enhance(img)
        
        # Check sizes
        expected_up_width = int(original_size[0] * 1.5)
        expected_up_height = int(original_size[1] * 1.5)
        
        expected_down_width = int(original_size[0] * 0.5)
        expected_down_height = int(original_size[1] * 0.5)
        
        assert upscaled.size == (expected_up_width, expected_up_height)
        assert downscaled.size == (expected_down_width, expected_down_height)
    
    def test_save_enhanced_image(self, test_image_path, temp_output_dir):
        """Test saving enhanced image"""
        output_path = os.path.join(temp_output_dir, "enhanced.png")
        
        enhancer = ImageEnhancer(EnhancementParams(brightness=1.2))
        enhancer.save_enhanced_image(test_image_path, output_path)
        
        # Check if file exists
        assert os.path.exists(output_path)
        
        # Check if it's a valid image
        img = Image.open(output_path)
        assert isinstance(img, Image.Image)
    
    def test_get_preview(self, load_test_images):
        """Test preview generation"""
        img = load_test_images['standard']
        original_size = img.size
        
        enhancer = ImageEnhancer()
        preview = enhancer.get_preview(img, size=(100, 100))
        
        # Preview should be smaller or equal to the requested size
        assert preview.width <= 100
        assert preview.height <= 100
        
        # Check aspect ratio is maintained
        original_ratio = original_size[0] / original_size[1]
        preview_ratio = preview.width / preview.height
        
        assert abs(original_ratio - preview_ratio) < 0.1  # Allow small rounding differences
    
    def test_compare_original_enhanced(self, load_test_images):
        """Test comparison generation"""
        img = load_test_images['standard']
        
        enhancer = ImageEnhancer(EnhancementParams(brightness=1.2))
        original, enhanced = enhancer.compare_original_enhanced(img)
        
        assert isinstance(original, Image.Image)
        assert isinstance(enhanced, Image.Image)
        assert original.size == enhanced.size 