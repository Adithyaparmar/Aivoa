import { useDispatch, useSelector } from 'react-redux';
import { fieldChanged, formReset } from './complaintSlice';
import { saveComplaint } from '../../api/client';
import { saveStarted, saveSucceeded, saveFailed } from './complaintSlice';

const FIELD_GROUPS = [
  {
    title: '1. Origin & Customer Details',
    fields: [
      { name: 'complaintSource', label: 'Complaint Source' },
      { name: 'customerName', label: 'Customer Name' },
    ],
  },
  {
    title: '2. Product & Batch Identification',
    fields: [
      { name: 'productName', label: 'Product Name' },
      { name: 'productStrengthGrade', label: 'Product Strength/Grade' },
      { name: 'batchLotNumber', label: 'Batch/Lot Number' },
      { name: 'manufacturingDate', label: 'Manufacturing Date', type: 'date' },
      { name: 'expiryDate', label: 'Expiry Date', type: 'date' },
      { name: 'quantityAffected', label: 'Quantity Affected' },
    ],
  },
  {
    title: '3. Complaint Details',
    fields: [
      { name: 'complaintType', label: 'Complaint Type' },
      { name: 'complaintDate', label: 'Complaint Date', type: 'date' },
      {
        name: 'complaintDescription',
        label: 'Detailed Complaint Description',
        fullWidth: true,
        multiline: true,
      },
    ],
  },
  {
    title: '4. Initial Assessment & Priority',
    fields: [
      {
        name: 'initialSeverity',
        label: 'Initial Severity',
        type: 'select',
        options: ['', 'Low', 'Medium', 'High', 'Critical'],
      },
      { name: 'priority', label: 'Priority' },
    ],
  },
];

export default function ComplaintForm() {
  const dispatch = useDispatch();
  const { fields, status } = useSelector((state) => state.complaint);

  const handleChange = (name) => (e) => {
    dispatch(fieldChanged({ name, value: e.target.value }));
  };

  const handleReset = () => dispatch(formReset());

  const handleSave = async () => {
    dispatch(saveStarted());
    try {
      await saveComplaint(fields);
      dispatch(saveSucceeded());
    } catch (err) {
      dispatch(saveFailed(err.message));
    }
  };

  return (
    <section className="panel complaint-panel">
      <header className="panel-header">
        <div>
          <h2>Log Customer Complaint</h2>
          <p className="panel-subtitle">API &amp; PDF Quality Assurance Module</p>
        </div>
        <span className={`status-pill status-${status.toLowerCase().replace(' ', '-')}`}>
          {status}
        </span>
      </header>

      <form
        className="complaint-form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSave();
        }}
      >
        {FIELD_GROUPS.map((group) => (
          <fieldset key={group.title}>
            <legend>{group.title}</legend>
            <div className="field-grid">
              {group.fields.map((f) => (
                <label
                  key={f.name}
                  className={f.fullWidth ? 'field field-full' : 'field'}
                >
                  {f.label}
                  {f.type === 'select' ? (
                    <select value={fields[f.name]} onChange={handleChange(f.name)}>
                      {f.options.map((opt) => (
                        <option key={opt} value={opt}>
                          {opt || 'Select…'}
                        </option>
                      ))}
                    </select>
                  ) : f.multiline ? (
                    <textarea
                      rows={4}
                      value={fields[f.name]}
                      onChange={handleChange(f.name)}
                      placeholder="Awaiting AI extraction…"
                    />
                  ) : (
                    <input
                      type={f.type || 'text'}
                      value={fields[f.name]}
                      onChange={handleChange(f.name)}
                      placeholder={f.type === 'date' ? undefined : 'Awaiting AI extraction…'}
                    />
                  )}
                </label>
              ))}
            </div>
          </fieldset>
        ))}

        <div className="form-actions">
          <button type="button" className="btn btn-ghost" onClick={handleReset}>
            Reset Form
          </button>
          <button type="submit" className="btn btn-primary">
            Save Complaint
          </button>
        </div>
      </form>
    </section>
  );
}
