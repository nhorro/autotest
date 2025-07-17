import argparse
from . import record, play
from . import screenshot
from . import window

def main():
    parser = argparse.ArgumentParser(description="autotest - UI automation")
    subparsers = parser.add_subparsers(dest="command")

    parser_record = subparsers.add_parser("record")
    parser_record.add_argument("-o", "--output", default="events.json")

    parser_play = subparsers.add_parser("play")
    parser_play.add_argument("-i", "--input", default="events.json")
    
    parser_capture = subparsers.add_parser("screenshot")
    parser_capture.add_argument("-o", "--output", required=True)
    parser_capture.add_argument("-m", "--monitor", type=int, default=None)
    parser_capture.add_argument("-w", "--window-title", default=None)

    parser_annotate = subparsers.add_parser("annotate", help="Anotar regiones sobre una imagen")
    parser_annotate.add_argument("-i", "--input", required=True, help="Imagen base")
    parser_annotate.add_argument("-o", "--output", default="annotations.json", help="Archivo de salida")

    subparsers.add_parser("list-windows", help="List window titles")

    parser_annotate = subparsers.add_parser("annotate", help="Anotar regiones sobre una imagen")
    parser_annotate.add_argument("-i", "--input", required=True, help="Imagen base")
    parser_annotate.add_argument("-o", "--output", default="annotations.json", help="Archivo de salida")



    args = parser.parse_args()

    if args.command == "record":
        record(args.output)
    elif args.command == "play":
        play(args.input)
    elif args.command == "screenshot":
        if args.window_title:
            screenshot.capture_window(args.output, args.window_title)
        else:
            monitor = args.monitor if args.monitor is not None else 1
            screenshot.capture_monitor(args.output, monitor)
    elif args.command == "list-windows":
        for t in window.list_open_window_titles():
            print(t)
    elif args.command == "annotate":
        from .annotate import annotate_image
        annotate_image(args.input, args.output)            
    else:
        parser.print_help()
