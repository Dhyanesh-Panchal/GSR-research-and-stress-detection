# Summary for preprocessing of the Data.

# Dataset Description
#### CASE Dataset description:
- [CASE_2019](https://springernature.figshare.com/articles/dataset/CASE_Dataset-full/8869157?backTo=/collections/A_dataset_of_continuous_affect_annotations_and_physiological_signals_for_emotion_analysis/4260668) is collected on 30 subjects with various sensors (one of them is GSR) on 12 different videos.
- Data is available in linearly interpolated and raw form.
- Sensor data is of 1000 Hz and annotation data (Valence Arousal) is of 20Hz


---
### Insights on GSR Sensor and EDA
- It measures the EDA activities, i.e. it measures the Skin Conductance(μS) which is directly influenced by dermal(sweat) activities.
- GSR is one of the sensors usually used with other physiological sensors due to its insufficient data provision on valance level.
- GSR data is a time series data.
- Simply, it provides data related to sensitivity/intensity of the emotion rather than taste of the emotion.
- But the paper suggests that GSR alone can provide up to 99.44% accuracy for (happy-sad classification).  

---
### Model used and Features required from the data
- Convolutional Neural Network(CNN) is used for classifying.
- Our Labels (valence-arousal) are also classified using 1d K-means.  (Mapping Function pg.no:22)
- **Features of GSR Signal**:
    - There are two components derived from the GSR signals: tonic that is related to the slow changes and phasic connected to the rapid change
    1. *Phasic Component*:
        - It is related to Fast changes of the data.
        - The phasic component is responsible for *skin conductance responses (SCRs)*, which are relatively fast variations in the GSR signal (order of seconds).
        - SCRs are the fast changes or peaks that can be seen.
            - SCRs can be divided into two:
                1.  event-related SCR (ER-SCR)
                2.  non-specific SCR (NS-SCR).
            - ER-SCRs can be created in reaction to a specific event and they are the most frequent measure for relating changes in emotional arousal to particular stimuli in researches.
            - *The apparent variation in ER-SCRs is SCR peaks that happen between 1 and 5 seconds after emotional stimuli begin.*
    2. *Tonic Component*:
        - The tonic component in a GSR signal is typically considered to be the background level of activity on top of which fast GSR responses emerge.
        - Individuals' baseline tonic levels vary greatly, often ranging from 2µS to 20µS.


- Also for the destructuring of the faetures from the Time-Series, Wavelet transform is a key technique, which I tried to explore and honestly got lost :)
- My Notes on **Continous Wavelet Transform(CWT)** is in [Notes.ipynb](./Notes.ipynb)

#### Training phase
- The CNN network is a 5-layer network that includes three packed Convolution-Max-Pooling layers and two Dense layers at the end that are the layer of outputs.
- In total 5 inputs are given to CNN model:
    1. Deconstructed phasic GSR
    2. Continous Wavelet Transform (CWT) using ricker (Mexican Hat wavelet).
    3. Spectral Flux (not explored yet)
    4. Stastical Features:
        - Mean
        - Variance
        - Skewness
        - Kurtosis
    5. Time Series Responce (not explored yet).
- Output is 2 values: Valence-Arousal.