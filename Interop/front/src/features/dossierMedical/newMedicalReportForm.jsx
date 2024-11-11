import React, {useEffect, useState} from 'react';
import {useAddNewMedicalReportMutation} from './medicalReportsApiSlice';
import {useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faSave} from '@fortawesome/free-solid-svg-icons';
import TextField from '@mui/material/TextField';

const NewMedicalReportForm = () => {
  console.log("NewMedicalReportForm mounted"); // Ajoutez ceci pour voir si le composant est bien monté

  const [addNewMedicalReport, {isLoading, isSuccess}] = useAddNewMedicalReportMutation();
  const navigate = useNavigate();

  const patientID = window.location.href.split("/")[5];
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    if (isSuccess) {
      navigate(`/dash/patients/${patientID}/reports`);
    }
  }, [isSuccess, navigate, patientID]);

  const handleSave = async (e) => {
    e.preventDefault();
    let result = await addNewMedicalReport({patient_id: patientID, title, content});
    console.log(result);
  };

  return (
      <form onSubmit={handleSave}>
        <h2>Add New Medical Report</h2>
        <TextField
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            fullWidth
            required
        />
        <TextField
            label="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            multiline
            rows={4}
            fullWidth
            required
        />
        <button type="submit">
          <FontAwesomeIcon icon={faSave}/> Save Report
        </button>
      </form>
  );
};

export default NewMedicalReportForm;
