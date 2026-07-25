import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  inputMode: 'idle', // idle | file | text
  fileName: null,
  pastedText: '',
  extraction: {
    inProgress: false,
    progressPct: 0,
    error: null,
  },
  chat: {
    messages: [
      {
        role: 'assistant',
        text: 'Upload a complaint document or paste text above. I will automatically extract the key details and populate the form for you.',
      },
    ],
    pending: false,
  },
};

const aiAssistantSlice = createSlice({
  name: 'aiAssistant',
  initialState,
  reducers: {
    fileSelected(state, action) {
      state.inputMode = 'file';
      state.fileName = action.payload;
      state.pastedText = '';
    },
    textPasted(state, action) {
      state.inputMode = 'text';
      state.pastedText = action.payload;
      state.fileName = null;
    },
    inputCleared(state) {
      state.inputMode = 'idle';
      state.fileName = null;
      state.pastedText = '';
    },
    extractionStarted(state) {
      state.extraction.inProgress = true;
      state.extraction.progressPct = 0;
      state.extraction.error = null;
    },
    extractionProgressed(state, action) {
      state.extraction.progressPct = action.payload;
    },
    extractionSucceeded(state) {
      state.extraction.inProgress = false;
      state.extraction.progressPct = 100;
    },
    extractionFailed(state, action) {
      state.extraction.inProgress = false;
      state.extraction.error = action.payload;
    },
    chatMessageSent(state, action) {
      state.chat.messages.push({ role: 'user', text: action.payload });
      state.chat.pending = true;
    },
    chatMessageReceived(state, action) {
      state.chat.messages.push({ role: 'assistant', text: action.payload });
      state.chat.pending = false;
    },
  },
});

export const {
  fileSelected,
  textPasted,
  inputCleared,
  extractionStarted,
  extractionProgressed,
  extractionSucceeded,
  extractionFailed,
  chatMessageSent,
  chatMessageReceived,
} = aiAssistantSlice.actions;

export default aiAssistantSlice.reducer;
