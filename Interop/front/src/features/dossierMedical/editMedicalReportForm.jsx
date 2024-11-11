import React, {useEffect, useState} from 'react';
import {useUpdateMedicalReportMutation} from './medicalReportsApiSlice.jsx';
import {useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faSave} from '@fortawesome/free-solid-svg-icons';
import TextField from '@mui/material/TextField';

const EditMedicalReportForm = ({report, doctors, patientID}) => {
    const [updateMedicalReport, {isLoading, isSuccess, isError, error}] = useUpdateMedicalReportMutation();
  const navigate = useNavigate();

    // Initialisation des états pour les champs du formulaire
    const [title, setTitle] = useState(report.title);
    const [content, setContent] = useState(report.content);

  useEffect(() => {
      if (isSuccess) {
          setTitle('');
          setContent('');
          setDoctorId('');
          navigate(`/patients/${patientID}/reports`);
      }
  }, [isSuccess, navigate, patientID]);

    const onTitleChanged = (e) => setTitle(e.target.value);
    const onContentChanged = (e) => setContent(e.target.value);

    const canSave = [title, content].every(Boolean) && !isLoading;

    const onSaveReportClicked = async (e) => {
    e.preventDefault();
        if (canSave) {
            try {
                await updateMedicalReport({
                    id: report.id,
                    patient_id: patientID,
                    title,
                    content
                }).unwrap();
                alert('Medical report updated successfully!');
            } catch (err) {
                console.error('Failed to update medical report:', err);
                alert('Error updating report! Please try again.');
            }
        } else {
            alert('Please fill out all fields.');
    }
  };

    const errClass = isError ? "errmsg" : "offscreen";
    const errContent = error?.data?.message ?? '';

    const contentForm = (
        <>
            <p className={errClass}>{errContent}</p>
            <form className="form" onSubmit={(e) => e.preventDefault()}>
                <div className="form__title-row">
                    <h2>Edit Medical Report [ID: {report.id}]</h2>
                    <div className="form__action-buttons">
                        <button
                            className="icon-button"
                            title="Save"
                            onClick={onSaveReportClicked}
                            disabled={!canSave}
                        >
                            <FontAwesomeIcon icon={faSave}/>
                        </button>
                    </div>
                </div>

                <div className="medical-report-form">
                    <TextField
                        label="Report Title"
                        name="title"
                        variant="outlined"
                        value={title}
                        onChange={onTitleChanged}
                        fullWidth
                        required
                        margin="normal"
                    />

                    <TextField
                        label="Report Content"
                        name="content"
                        variant="outlined"
                        value={content}
                        onChange={onContentChanged}
                        fullWidth
                        required
                        multiline
                        rows={4}
                        margin="normal"
                    />
                </div>
      </form>
        </>
  );

    return contentForm;
};

export default EditMedicalReportForm;
