import click
import json
 
'''
@click.group(<name>) creates a command that instantiates a group class
a group is intended to be a set of related commands
@click.argument(<argument name>) tells us that we will be passing an argument
and referring to that argument in the function by the name we pass it
@click.pass_context tells the group command that we're going to be using
the context, the context is not visible to the command unless we pass this
 
In our example we'll name our group "cli"
'''
@click.group("cli")
@click.pass_context
@click.argument("document")
def cli(ctx, document):
   """An example CLI for interfacing with a document"""
   _stream = open(document)
   _dict = json.load(_stream)
   _stream.close()
   ctx.obj = _dict
 
def main():
   cli(prog_name="python3")
 
if __name__ == '__main__':
   main()