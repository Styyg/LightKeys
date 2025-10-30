# LightKeys

**LightKeys** is a project running on a **Raspberry Pi** that controls an **RGBW LED strip** using a **MIDI piano** as input.  
Each note triggers real-time lighting effects, based on customizable *color modes* and *effect modes*, configurable through a **local web interface**.


## Installation

### 1. Clone the project
```bash
git clone https://github.com/Styyg/LightKeys.git
cd LightKeys
```

### 2. Create a virtual environnement
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
For Raspberry Pi
```bash
pip install -r requirements.txt
```

For other OS like Windows (server only, midi and leds are simulated)
```bash
pip install -r requirements-dev.txt
```

### 4. Run LightKeys
```bash
sudo venv/bin/python -m lightkeys
```
