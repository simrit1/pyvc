from setuptools import find_packages, setup

setup(
    name='pyvc',
    version='0.0.0',
    author='zakarh 2021',
    description='Package for voice controls in Python',
    long_description=open('README.md').read(),
    license='LICENSE',
    keywords="python voice-commands speech-recognition tts stt",
    install_requires=["PyAudio", "pyttsx3", "SpeechRecognition"],

    package_dir={'': 'src'},
    packages=find_packages('src', exclude='docs'),

    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Microsoft :: Windows",
    ]
)
