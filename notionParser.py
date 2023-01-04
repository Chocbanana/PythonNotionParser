#!/usr/bin/env python3

from argparse import ArgumentParser
import pathlib

from notion2Model import *

if __name__ == "__main__":
    parser = ArgumentParser(
                description = "A parser for the website Notion.so's exported data, to JSON or a native Python object for further transforming.")

    parser.add_argument("export_type", help="If exported data to parse was in html or md+csv style, or both", choices=["html", "mdcsv"])
    parser.add_argument("--html-path", type=pathlib.Path, help="If html or both was specified, the dir path of data")
    parser.add_argument("--mdcsv-path", type=pathlib.Path, help="If mdcsv or both was specified, the dir path of data")
    parser.add_argument("-o", "--out-path", type=pathlib.Path, required=True, help="The directory to store results in")
    parser.add_argument("--one-file", action="store_true", help="Whether to generate just one file with all data or to preserve Notion's export file structure")

    args = parser.parse_args()

    ## Arg validation
    if args.export_type == "html":
        ToModel.validate_path(args.html_path)
    elif args.export_type == "mdcsv":
        ToModel.validate_path(args.mdcsv_path)
    elif args.export_type == "both":
        ToModel.validate_path(args.html_path)
        ToModel.validate_path(args.mdcsv_path)

    # Make sure appropriate paths given for selected export type

    # Validate if out path already has files

    ## Parse into model
    if args.export_type == "html":
        pass
    elif args.export_type == "mdcsv":
        mdcsv_parser = MdCsv2Model(args.mdcsv_path)
        mdcsv_parser.parse()
    elif args.export_type == "both":
        pass


    print(args)
