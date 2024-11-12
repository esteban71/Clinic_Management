import React from 'react';
import {useParams} from 'react-router-dom';
import EditMedicalReportForm from './editMedicalReportForm';
import {useGetMedicalReportsQuery} from './medicalReportsApiSlice.jsx';

const EditMedicalReport = () => {
    const {id, reportID} = useParams();
    const {data: medicalReports, isLoading, isSuccess, isError, error} = useGetMedicalReportsQuery(id, {
        pollingInterval: 15000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true,
    });

    const report = medicalReports.entities[reportID];

    const content = report ? <EditMedicalReportForm report={report} patientID={id}/> :
        <p>Loading...</p>;

    console.log('content', content);

    return content;
};

export default EditMedicalReport;
