#!/usr/bin/env python3
import argparse
import os
import sys
from typing import List, Optional, Dict, Any
from PIL import Image
import json

# Add parent directory to path to allow module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.img_enhance.enhancer import ImageEnhancer, EnhancementParams
from src.img_enhance.auto_enhance import auto_enhance_image, batch_auto_enhance
from src.img_enhance.utils import (
    save_params_to_json, 
    load_params_from_json, 
    create_comparison_image,
    plot_enhancement_metrics,
    get_supported_formats
)

def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Image Enhancement for OCR')
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Operation mode')
    
    # Auto-enhance mode
    auto_parser = subparsers.add_parser('auto', help='Automatically enhance images')
    auto_parser.add_argument('input_path', help='Input image path or directory')
    auto_parser.add_argument('--output-path', '-o', help='Output image path or directory')
    auto_parser.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
    auto_parser.add_argument('--compare', '-c', action='store_true', help='Create comparison images')
    auto_parser.add_argument('--plot', '-p', action='store_true', help='Plot enhancement metrics')
    
    # Manual enhance mode
    manual_parser = subparsers.add_parser('manual', help='Manually enhance images with specified parameters')
    manual_parser.add_argument('input_path', help='Input image path or directory')
    manual_parser.add_argument('--output-path', '-o', help='Output image path or directory')
    manual_parser.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
    manual_parser.add_argument('--compare', '-c', action='store_true', help='Create comparison images')
    manual_parser.add_argument('--plot', '-p', action='store_true', help='Plot enhancement metrics')
    
    # Enhancement parameters
    manual_parser.add_argument('--brightness', '-b', type=float, default=1.0, help='Brightness (0.5-1.5)')
    manual_parser.add_argument('--contrast', type=float, default=1.0, help='Contrast (0.5-2.0)')
    manual_parser.add_argument('--sharpness', '-s', type=float, default=1.0, help='Sharpness (0.0-2.0)')
    manual_parser.add_argument('--color', type=float, default=1.0, help='Color (0.0-2.0)')
    manual_parser.add_argument('--denoise', action='store_true', help='Apply denoising')
    manual_parser.add_argument('--binarize', action='store_true', help='Binarize image (black and white)')
    manual_parser.add_argument('--binarize-threshold', type=int, default=128, help='Binarization threshold (0-255)')
    manual_parser.add_argument('--deskew', action='store_true', help='Deskew image')
    manual_parser.add_argument('--resize-factor', type=float, help='Resize factor (e.g., 1.5 for 150%)')
    
    # Parameter file
    manual_parser.add_argument('--params-file', help='JSON file with enhancement parameters')
    manual_parser.add_argument('--save-params', help='Save parameters to JSON file')
    
    # Batch processing
    batch_parser = subparsers.add_parser('batch', help='Batch process images')
    batch_parser.add_argument('input_dir', help='Input directory containing images')
    batch_parser.add_argument('--output-dir', '-o', required=True, help='Output directory for enhanced images')
    batch_parser.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
    batch_parser.add_argument('--mode', choices=['auto', 'manual'], default='auto', help='Enhancement mode')
    batch_parser.add_argument('--params-file', help='JSON file with enhancement parameters (for manual mode)')
    batch_parser.add_argument('--compare', '-c', action='store_true', help='Create comparison images')
    
    # Preview mode
    preview_parser = subparsers.add_parser('preview', help='Generate preview grid with different enhancements')
    preview_parser.add_argument('input_path', help='Input image path')
    preview_parser.add_argument('--output-path', '-o', required=True, help='Output image path')
    
    return parser.parse_args()

def get_image_paths(input_path: str, recursive: bool = False) -> List[str]:
    """
    Get list of image file paths
    
    Args:
        input_path: Input path (file or directory)
        recursive: Whether to process directories recursively
        
    Returns:
        List of image file paths
    """
    supported_formats = get_supported_formats()
    
    if os.path.isfile(input_path):
        # Single file
        _, ext = os.path.splitext(input_path.lower())
        if ext in supported_formats:
            return [input_path]
        else:
            return []
    elif os.path.isdir(input_path):
        # Directory
        image_paths = []
        
        if recursive:
            # Walk through all subdirectories
            for root, _, files in os.walk(input_path):
                for file in files:
                    _, ext = os.path.splitext(file.lower())
                    if ext in supported_formats:
                        image_paths.append(os.path.join(root, file))
        else:
            # Just this directory
            for file in os.listdir(input_path):
                _, ext = os.path.splitext(file.lower())
                if ext in supported_formats:
                    image_paths.append(os.path.join(input_path, file))
        
        return image_paths
    else:
        raise FileNotFoundError(f"Input path not found: {input_path}")

def get_output_path(input_path: str, output_path: Optional[str], suffix: str = "_enhanced") -> str:
    """
    Determine output path for an enhanced image
    
    Args:
        input_path: Input image path
        output_path: Specified output path (may be None)
        suffix: Suffix to add to filename
        
    Returns:
        Output path for enhanced image
    """
    if output_path is None:
        # Use same directory as input, add suffix to filename
        dirname = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        base, ext = os.path.splitext(filename)
        return os.path.join(dirname, f"{base}{suffix}{ext}")
    elif os.path.isdir(output_path):
        # Output is a directory, put file inside
        filename = os.path.basename(input_path)
        base, ext = os.path.splitext(filename)
        return os.path.join(output_path, f"{base}{suffix}{ext}")
    else:
        # Output is a file path
        return output_path

def auto_mode(args):
    """Auto-enhance mode processing"""
    # Get image paths
    image_paths = get_image_paths(args.input_path, args.recursive)
    
    if not image_paths:
        print("No supported image files found.")
        return
    
    print(f"Found {len(image_paths)} image(s).")
    
    # Process each image
    for img_path in image_paths:
        print(f"Processing: {img_path}")
        
        # Auto-enhance
        enhanced = auto_enhance_image(img_path)
        
        # Determine output path and save
        if args.output_path:
            if os.path.isdir(args.output_path):
                # Output directory specified
                filename = os.path.basename(img_path)
                base, ext = os.path.splitext(filename)
                output_path = os.path.join(args.output_path, f"{base}_enhanced{ext}")
            else:
                # Single file output (only valid for first image)
                output_path = args.output_path
        else:
            # No output specified, use input directory
            dirname = os.path.dirname(img_path)
            filename = os.path.basename(img_path)
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(dirname, f"{base}_enhanced{ext}")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save enhanced image
        enhanced.save(output_path)
        print(f"Saved: {output_path}")
        
        # Create comparison if requested
        if args.compare:
            original = Image.open(img_path).convert('RGB')
            comparison = create_comparison_image(original, enhanced)
            
            # Determine comparison output path
            comp_path = os.path.splitext(output_path)[0] + "_comparison.png"
            comparison.save(comp_path)
            print(f"Saved comparison: {comp_path}")
        
        # Plot metrics if requested
        if args.plot:
            # Analyze and determine parameters
            from src.img_enhance.auto_enhance import analyze_image, determine_optimal_params
            metrics = analyze_image(img_path)
            params = determine_optimal_params(metrics)
            
            # Create plot
            plot_path = os.path.splitext(output_path)[0] + "_metrics.png"
            plot_enhancement_metrics(img_path, enhanced, params, show_plot=False, save_path=plot_path)
            print(f"Saved metrics plot: {plot_path}")

def manual_mode(args):
    """Manual enhancement mode processing"""
    # Load parameters from file if specified, otherwise use command-line args
    if args.params_file:
        try:
            params = load_params_from_json(args.params_file)
            print(f"Loaded parameters from: {args.params_file}")
        except Exception as e:
            print(f"Error loading parameters: {e}")
            return
    else:
        # Create parameters from command-line arguments
        params = EnhancementParams(
            brightness=args.brightness,
            contrast=args.contrast,
            sharpness=args.sharpness,
            color=args.color,
            denoise=args.denoise,
            binarize=args.binarize,
            binarize_threshold=args.binarize_threshold,
            deskew=args.deskew,
            resize_factor=args.resize_factor
        )
    
    # Save parameters if requested
    if args.save_params:
        try:
            save_params_to_json(params, args.save_params)
            print(f"Saved parameters to: {args.save_params}")
        except Exception as e:
            print(f"Error saving parameters: {e}")
    
    # Get image paths
    image_paths = get_image_paths(args.input_path, args.recursive)
    
    if not image_paths:
        print("No supported image files found.")
        return
    
    print(f"Found {len(image_paths)} image(s).")
    
    # Create enhancer
    enhancer = ImageEnhancer(params)
    
    # Process each image
    for img_path in image_paths:
        print(f"Processing: {img_path}")
        
        # Enhance
        enhanced = enhancer.enhance(img_path)
        
        # Determine output path and save
        if args.output_path:
            if os.path.isdir(args.output_path):
                # Output directory specified
                filename = os.path.basename(img_path)
                base, ext = os.path.splitext(filename)
                output_path = os.path.join(args.output_path, f"{base}_enhanced{ext}")
            else:
                # Single file output (only valid for first image)
                output_path = args.output_path
        else:
            # No output specified, use input directory
            dirname = os.path.dirname(img_path)
            filename = os.path.basename(img_path)
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(dirname, f"{base}_enhanced{ext}")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save enhanced image
        enhanced.save(output_path)
        print(f"Saved: {output_path}")
        
        # Create comparison if requested
        if args.compare:
            original = Image.open(img_path).convert('RGB')
            comparison = create_comparison_image(original, enhanced, params)
            
            # Determine comparison output path
            comp_path = os.path.splitext(output_path)[0] + "_comparison.png"
            comparison.save(comp_path)
            print(f"Saved comparison: {comp_path}")
        
        # Plot metrics if requested
        if args.plot:
            # Create plot
            plot_path = os.path.splitext(output_path)[0] + "_metrics.png"
            plot_enhancement_metrics(img_path, enhanced, params, show_plot=False, save_path=plot_path)
            print(f"Saved metrics plot: {plot_path}")

def batch_mode(args):
    """Batch processing mode"""
    # Get image paths
    image_paths = get_image_paths(args.input_dir, args.recursive)
    
    if not image_paths:
        print("No supported image files found.")
        return
    
    print(f"Found {len(image_paths)} image(s).")
    
    # Create output directory if needed
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.mode == 'auto':
        # Auto batch mode
        output_paths = batch_auto_enhance(image_paths, args.output_dir)
        print(f"Enhanced {len(output_paths)} images in auto mode.")
        
        # Create comparisons if requested
        if args.compare:
            comparison_dir = os.path.join(args.output_dir, "comparisons")
            os.makedirs(comparison_dir, exist_ok=True)
            
            for i, (input_path, output_path) in enumerate(zip(image_paths, output_paths)):
                print(f"Creating comparison {i+1}/{len(image_paths)}")
                original = Image.open(input_path).convert('RGB')
                enhanced = Image.open(output_path).convert('RGB')
                
                comparison = create_comparison_image(original, enhanced)
                
                # Save comparison
                filename = os.path.basename(input_path)
                base, _ = os.path.splitext(filename)
                comp_path = os.path.join(comparison_dir, f"{base}_comparison.png")
                comparison.save(comp_path)
    else:
        # Manual batch mode
        if args.params_file:
            try:
                params = load_params_from_json(args.params_file)
                print(f"Loaded parameters from: {args.params_file}")
            except Exception as e:
                print(f"Error loading parameters: {e}")
                return
        else:
            # Use default parameters
            params = EnhancementParams()
        
        # Create enhancer
        enhancer = ImageEnhancer(params)
        
        # Process each image
        for img_path in image_paths:
            print(f"Processing: {img_path}")
            
            # Enhance
            enhanced = enhancer.enhance(img_path)
            
            # Determine output path
            filename = os.path.basename(img_path)
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(args.output_dir, f"{base}_enhanced{ext}")
            
            # Save enhanced image
            enhanced.save(output_path)
            
            # Create comparison if requested
            if args.compare:
                comparison_dir = os.path.join(args.output_dir, "comparisons")
                os.makedirs(comparison_dir, exist_ok=True)
                
                original = Image.open(img_path).convert('RGB')
                comparison = create_comparison_image(original, enhanced, params)
                
                # Save comparison
                comp_path = os.path.join(comparison_dir, f"{base}_comparison.png")
                comparison.save(comp_path)

def preview_mode(args):
    """Preview grid mode"""
    from src.img_enhance.auto_enhance import get_enhancement_preview_grid
    
    # Check if input file exists
    if not os.path.isfile(args.input_path):
        print(f"Input file not found: {args.input_path}")
        return
    
    # Generate preview grid
    preview_grid = get_enhancement_preview_grid(args.input_path)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(os.path.abspath(args.output_path)), exist_ok=True)
    
    # Save preview grid
    preview_grid.save(args.output_path)
    print(f"Saved preview grid: {args.output_path}")

def main():
    """Main entry point"""
    args = parse_args()
    
    if args.mode == 'auto':
        auto_mode(args)
    elif args.mode == 'manual':
        manual_mode(args)
    elif args.mode == 'batch':
        batch_mode(args)
    elif args.mode == 'preview':
        preview_mode(args)
    else:
        print("Please specify a mode: auto, manual, batch, or preview")

if __name__ == '__main__':
    main() 