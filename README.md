# BeEPy
Behavioral + electrophysiology analyses in python

For a MATLAB equivalent, see CMBHOME (https://github.com/hasselmonians/CMBHOME)

## Data structure
The main datastructures are:
- `beepy.Unit`: Holds spike times, and indexes into Lfp and Session to get variables at spike times
  - `Unit.data`: A *dynamic dictionary* of variables (from LFP and behavior) at spike time
- `beepy.Lfp`: Holds LFP data
  - `Lfp.data`: A *dynamic dictionary* of time-varying variables
- `beepy.Session`: Holds behavioral data, session metadata, a dictionary of Units, and a dictionary of LFPs. 
  - `Session.data`: *Dynamic dictionary* of behavioral variables
  - `Session.active_unit`: *Key* (eg: [0,0]) telling which unit to parse
  - `Session.active_lfp`: *Key* (eg: [0]) telling which LFP channel to parse
  - `Session.epoch`: *List* of time periods, in seconds, telling what behavioral periods to look at (eg: trials)
  - `Session.mode`: When running with multiple epochs, should an analysis concatenate into one large epoch (`session.mode = 'cat'`), or evaluate seperately for each (`session.mode = 'map'`)

- The primary functionality of the datastructures is the introduction of *dynamic dictionaries*. These fields take some underlying time-varying signal, and index into it based on the active LFP, active Unit, and epoch.

## Time variables:
- LFP and Session come with a small number of predefined variables at load time:
  - LFP
    - `ts`: Time stamp (seconds)
    - `signal`: Raw trace (mV?)
  - Session
    - `x`: X position of animal (cm)
    - `y`: Y position of animal (cm)
    - `hd`: Head direction (radians)
- Methods exist for adding certain variables:
  - LFP
    - `add_band`: Adds the filtered signal and instantaneous frequency+phase+magnitude of a specific frequency band
  - Session
    - `vel`: Calculates  the Kalman filtered velocity, angular velocity, acceleration, and angular acceleration
- For any other variable `Lfp.add_custom` and `Session.add_custom` allow you to pass a variable with the same length as the underlying timestamps (along with a name for the key). These will be added to the dynamic dictionaries and calculated just as the built-in variables are.

## Analyses
- Analyses should accept a Session, respecting any states within it (eg: Session.epoch, Session.active_unit, Session.active_lfp)
- Broken up into submodules based on the nature of the analysis:
  - `Analyses.fields`: Receptive fields (# spikes / occupancy)
    - `Analyses.fields.ratemap`: 2D ratemap (default: x & y coordinates)
    - `Analyses.fields.headdir`: 1D polar ratemap (default: headdir)
  - `Analyses.lfp`: Phase locking, phase coding, and phase-coupling measures here ...

## IO
- Functions for importing from various external datastructures.
- Function for saving to a NeurodataWithoutBorders (.nwb) format.

## Installation:
`pip install -e git+git://github.com/wchapman/BeEPy/.git`
