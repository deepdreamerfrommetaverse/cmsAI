import { useGenerator } from './useGenerator';
export function useAgent() {
  // For Prompt Agent, we can reuse generation logic
  const generator = useGenerator();
  return { ...generator };
}
