import React, { useContext } from 'react';
import { PersonalizationContext } from '../../contexts/PersonalizationContext';

const PersonalizationButtons: React.FC = () => {
  const context = useContext(PersonalizationContext);

  if (!context) {
    return null;
  }

  const { learningMode, setLearningMode, difficulty, setDifficulty, focusArea, setFocusArea } = context;

  const modes = ['beginner', 'advanced'];
  const difficulties = ['basic', 'intermediate', 'advanced'];
  const focusAreas = ['theory', 'practice'];

  return (
    <div style={{ padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '8px', marginBottom: '20px' }}>
      <h3>Personalize Your Learning Experience</h3>

      <div style={{ marginBottom: '15px' }}>
        <strong>Learning Mode:</strong>
        {modes.map(mode => (
          <button
            key={mode}
            onClick={() => setLearningMode(mode)}
            style={{
              margin: '0 5px',
              padding: '5px 10px',
              backgroundColor: learningMode === mode ? '#007cba' : '#e0e0e0',
              color: learningMode === mode ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ marginBottom: '15px' }}>
        <strong>Difficulty Level:</strong>
        {difficulties.map(level => (
          <button
            key={level}
            onClick={() => setDifficulty(level)}
            style={{
              margin: '0 5px',
              padding: '5px 10px',
              backgroundColor: difficulty === level ? '#007cba' : '#e0e0e0',
              color: difficulty === level ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {level.charAt(0).toUpperCase() + level.slice(1)}
          </button>
        ))}
      </div>

      <div>
        <strong>Focus Area:</strong>
        {focusAreas.map(area => (
          <button
            key={area}
            onClick={() => setFocusArea(area)}
            style={{
              margin: '0 5px',
              padding: '5px 10px',
              backgroundColor: focusArea === area ? '#007cba' : '#e0e0e0',
              color: focusArea === area ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {area.charAt(0).toUpperCase() + area.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};

export default PersonalizationButtons;