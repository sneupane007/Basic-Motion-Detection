#!/usr/bin/env python3
"""
Main entry point for the Motion Detection Dashboard application
"""
import os
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motion Detection Dashboard")
    parser.add_argument("--mode", choices=["web", "detection", "all"], 
                        default="web",
                        help="Run mode: web (dashboard only), detection (motion detection only), or all (both)")
    
    args = parser.parse_args()
    
    if args.mode in ["web", "all"]:
        # Run web dashboard
        from src.app import run_app
        if args.mode == "all":
            # Run in a separate process
            pid = os.fork() if os.name != 'nt' else 0
            if pid == 0:  # Child process or Windows
                if os.name == 'nt':  # Windows doesn't support fork
                    import threading
                    import src.motion_detection.detection as motion_det
                    detection_thread = threading.Thread(target=motion_det.start_motion_detection)
                    detection_thread.daemon = True
                    detection_thread.start()
                run_app()
            else:  # Parent process (Unix/Linux/Mac)
                from src.motion_detection.detection import start_motion_detection
                start_motion_detection()
        else:
            # Just run the web app
            run_app()
    elif args.mode == "detection":
        # Run motion detection only
        from src.motion_detection.detection import start_motion_detection
        start_motion_detection()
    else:
        print(f"Unknown mode: {args.mode}")
        sys.exit(1) 