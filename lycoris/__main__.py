# this code runs the Lycoris CLI
import os, time, sys
import typer

app = typer.Typer()

@app.command()
def build(input_dir: str, output_dir: str):
    print(f"Building {input_dir} to {output_dir}")

app()