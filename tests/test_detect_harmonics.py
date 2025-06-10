import types
from corems.mass_spectrum.factory.MassSpectrumClasses import MassSpecfromFreq
from corems.encapsulation.factory.parameters import MSParameters
from corems.ms_peak.factory.MSPeakClasses import ICRMassPeak, PeakType


def create_ms_with_peaks(freq_abundance):
    ms = MassSpecfromFreq.__new__(MassSpecfromFreq)
    ms.parameters = MSParameters(use_defaults=True)
    ms.mspeaks = []
    ms.transient_settings = types.SimpleNamespace(qpd_enabled=0)
    for i, (freq, abundance) in enumerate(freq_abundance):
        peak = ICRMassPeak(
            1,
            freq,
            abundance,
            1000,
            10,
            (0, 0, 0),
            i,
            ms_parent=ms,
            exp_freq=freq,
        )
        ms.mspeaks.append(peak)
    return ms


def test_detect_harmonic_peaks():
    freq_abundance = [
        (1000, 1000),
        (2000, 800),
        (1100, 1000),
        (3300, 900),
        (1500, 1000),
        (6000, 700),
        (2500, 1000),
    ]
    ms = create_ms_with_peaks(freq_abundance)
    ms.detect_harmonic_peaks(tol=0)
    harmonic_idx = {1, 3, 5}
    for idx, peak in enumerate(ms.mspeaks):
        if idx in harmonic_idx:
            assert peak.peak_type is PeakType.HARMONIC
        else:
            assert peak.peak_type is PeakType.REAL

