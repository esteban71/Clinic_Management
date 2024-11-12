import React from 'react';
import {useSelector} from 'react-redux';
import {useParams} from 'react-router-dom';
import EditMedicalReportForm from './editMedicalReportForm';
import {selectMedicalReportById} from './medicalReportsApiSlice.jsx';

const EditMedicalReport = () => {
    const {id} = useParams();
    const report = useSelector(state => selectMedicalReportById(state, id));

    const content = report && medecin ? <EditMedicalReportForm report={report}/> :
        <p>Loading...</p>;

    console.log('content', content);

    return content;
};

export default EditMedicalReport;
