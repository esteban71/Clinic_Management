import React, { useEffect, useState } from 'react';
import { useAddNewMedicalReportMutation } from './medicalReportsApiSlice';
import { useNavigate, useParams } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave } from '@fortawesome/free-solid-svg-icons';
import TextField from '@mui/material/TextField';

const NewMedicalReportForm = () => {
  const patientID = window.location.href.split('/')[5];
  const [addNewMedicalReport, { isLoading, isSuccess }] = useAddNewMedicalReportMutation();
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [date, setDate] = useState('');

  useEffect(() => {
    if (isSuccess) {
      navigate(`/dash/patients/${patientID}/reports`);
    }
  }, [isSuccess, navigate, patientID]);

  const handleSave = async (e) => {
    e.preventDefault();
    if (patientID && title && content) {
      try {
        const result = await addNewMedicalReport({
          patient_id: patientID, // Assure-toi que patientID est un nombre
          title,
          content,
          date
        }).unwrap();
        console.log(result);
      } catch (err) {
        console.error('Erreur lors de l\'envoi du rapport médical:', err);
      }
    } else {
      console.error('Missing fields:', { patient_id, title, content, date });
      alert('Please fill out all fields.');
    }
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
      <TextField
        label="Date"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        fullWidth
        required
      />
      <button type="submit" disabled={isLoading}>
        <FontAwesomeIcon icon={faSave} /> Save Report
      </button>
    </form>
  );
};

export default NewMedicalReportForm;
