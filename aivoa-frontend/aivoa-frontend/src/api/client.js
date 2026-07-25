import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

// Single contract point with the backend: send either a file or raw text,
// the LangGraph agent runs end-to-end, and the full resulting state comes
// back as JSON (extracted fields + completeness + risk + any bonus outputs).
export async function runComplaintGraph({ file, text }) {
  const formData = new FormData();
  if (file) formData.append('file', file);
  if (text) formData.append('text', text);

  const { data } = await api.post('/complaints/process', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: undefined, // set per-call if progress UI is wired up
  });
  return data;
}

export async function askAssistant({ question, complaintContext }) {
  const { data } = await api.post('/assistant/ask', {
    question,
    context: complaintContext,
  });
  return data;
}

export async function saveComplaint(fields, analysis) {
  const { data } = await api.post('/complaints', { fields, analysis: analysis ?? null });
  return data;
}

export default api;
