import { configureStore } from '@reduxjs/toolkit';
import complaintReducer from '../features/complaint/complaintSlice';
import aiAssistantReducer from '../features/aiAssistant/aiAssistantSlice';

export const store = configureStore({
  reducer: {
    complaint: complaintReducer,
    aiAssistant: aiAssistantReducer,
  },
});
