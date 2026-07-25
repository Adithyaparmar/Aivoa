import { useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fileSelected,
  textPasted,
  extractionStarted,
  extractionProgressed,
  extractionSucceeded,
  extractionFailed,
  chatMessageSent,
  chatMessageReceived,
} from './aiAssistantSlice';
import { fieldsPopulated } from '../complaint/complaintSlice';
import { runComplaintGraph, askAssistant } from '../../api/client';

export default function AIAssistantPanel() {
  const dispatch = useDispatch();
  const { fileName, extraction, chat } = useSelector((state) => state.aiAssistant);
  const fields = useSelector((state) => state.complaint.fields);
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);
  const [chatDraft, setChatDraft] = useState('');

  const runExtraction = async ({ file, text }) => {
    dispatch(extractionStarted());
    try {
      // Simple staged progress while the graph runs server-side; the backend
      // returns the final state in one shot per the single-endpoint contract.
      dispatch(extractionProgressed(10));
      const result = await runComplaintGraph({ file, text });
      dispatch(extractionProgressed(90));
      dispatch(fieldsPopulated(result.fields ?? {}));
      dispatch(extractionSucceeded());
    } catch (err) {
      dispatch(extractionFailed(err.message));
    }
  };

  const handleFile = (file) => {
    if (!file) return;
    dispatch(fileSelected(file.name));
    runExtraction({ file });
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const handlePasteSubmit = (e) => {
    e.preventDefault();
    const text = e.target.elements.pasteText.value.trim();
    if (!text) return;
    dispatch(textPasted(text));
    runExtraction({ text });
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    const question = chatDraft.trim();
    if (!question) return;
    dispatch(chatMessageSent(question));
    setChatDraft('');
    try {
      const { answer } = await askAssistant({ question, complaintContext: fields });
      dispatch(chatMessageReceived(answer));
    } catch {
      dispatch(chatMessageReceived('Sorry, I could not reach the assistant. Please try again.'));
    }
  };

  return (
    <section className="panel ai-panel">
      <header className="panel-header">
        <h2>AI Complaint Intake Assistant</h2>
        <span className="beta-pill">BETA</span>
      </header>

      <div
        className={`dropzone ${dragActive ? 'dropzone-active' : ''}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <p>
          Drag &amp; drop complaint document here
          <br />
          or{' '}
          <button
            type="button"
            className="link-btn"
            onClick={() => fileInputRef.current?.click()}
          >
            click to browse
          </button>
        </p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt,.eml"
          hidden
          onChange={(e) => handleFile(e.target.files?.[0])}
        />
        {fileName && <p className="file-chip">{fileName}</p>}
      </div>

      <div className="divider-or">OR</div>

      <form onSubmit={handlePasteSubmit} className="paste-form">
        <textarea
          name="pasteText"
          rows={3}
          placeholder="Paste Complaint Text / Email"
        />
        <button type="submit" className="btn btn-secondary">
          Paste Complaint Text / Email
        </button>
      </form>

      <p className="format-hint">Supported formats: PDF, DOCX, TXT, EML — Max size 10MB</p>

      {(extraction.inProgress || extraction.progressPct > 0) && (
        <div className="extraction-progress">
          <div className="progress-label">
            <span>Extraction Progress</span>
            <span>{extraction.progressPct}%</span>
          </div>
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{ width: `${extraction.progressPct}%` }}
            />
          </div>
          <p className="progress-note">
            {extraction.error
              ? extraction.error
              : 'Analyzing document content and extracting key details. Please wait, this may take a few moments.'}
          </p>
        </div>
      )}

      <div className="ai-assistant-chat">
        <h3>AI Assistant</h3>
        <div className="chat-messages">
          {chat.messages.map((m, i) => (
            <div key={i} className={`chat-bubble chat-${m.role}`}>
              {m.text}
            </div>
          ))}
          {chat.pending && <div className="chat-bubble chat-assistant">Thinking…</div>}
        </div>
        <form onSubmit={handleChatSubmit} className="chat-input-row">
          <input
            type="text"
            placeholder="Ask me anything about this complaint…"
            value={chatDraft}
            onChange={(e) => setChatDraft(e.target.value)}
          />
          <button type="submit" aria-label="Send">
            ➤
          </button>
        </form>
        <p className="disclaimer">AI responses may contain errors. Please verify information.</p>
      </div>
    </section>
  );
}
