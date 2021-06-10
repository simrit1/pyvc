# pyvc

This is a bare-bones Python package to create programs that listen and speak, or to add voice commands.

## Getting Started

**Prerequisites**

Requirements to use the package

- [Python 3.6](https://www.python.org/downloads/release/python-360/)

**Installing**

```shell
git clone https://github.com/zakarh/pyvc
cd path/pyvc
py -3.6 -m pip install .
```

## Usage

**pyvc** is simple to use when creating programs that listen and speak. 

**Example**

```shell
py -3.6 example.py
```

```python
from pyvc import PYVC

def main():
    bot = PYVC()

    @bot.command(phrase="Hello World", description="Say 'Hello World!'")
    def hello_world():
        bot.speak("Hello World!")
        
    @bot.command("Repeat after me", "Say what will be repeated back to you.")
    def hello_world():
        print("Say what I will repeat.")
        bot.speak(bot.listen())

    bot.start(debug=True)

if __name__ == "__main__":
    main()
```

## Limitations

This is a prototype. It was developed on Windows OS and so it may not work on other OS.

## License

[LICENSE](./LICENSE)
