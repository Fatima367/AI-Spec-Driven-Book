import React, { createContext, useState, ReactNode } from 'react';

interface PersonalizationContextType {
  learningMode: string;
  setLearningMode: (mode: string) => void;
  difficulty: string;
  setDifficulty: (difficulty: string) => void;
  focusArea: string;
  setFocusArea: (area: string) => void;
}

export const PersonalizationContext = createContext<PersonalizationContextType | undefined>(undefined);

interface PersonalizationProviderProps {
  children: ReactNode;
}

export const PersonalizationProvider: React.FC<PersonalizationProviderProps> = ({ children }) => {
  const [learningMode, setLearningMode] = useState<string>('beginner');
  const [difficulty, setDifficulty] = useState<string>('basic');
  const [focusArea, setFocusArea] = useState<string>('theory');

  return (
    <PersonalizationContext.Provider value={{
      learningMode,
      setLearningMode,
      difficulty,
      setDifficulty,
      focusArea,
      setFocusArea
    }}>
      {children}
    </PersonalizationContext.Provider>
  );
};