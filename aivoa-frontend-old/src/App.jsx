import ComplaintForm from './features/complaint/ComplaintForm';
import AIAssistantPanel from './features/aiAssistant/AIAssistantPanel';
import './styles/app.css';

export default function App() {
  return (
    <div className="app-shell">
      <ComplaintForm />
      <AIAssistantPanel />
    </div>
  );
}
