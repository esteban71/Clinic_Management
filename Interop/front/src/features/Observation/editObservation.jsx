import React from 'react';
import {useParams} from 'react-router-dom';
import EditObservationForm from './editObservationForm.jsx';
import {useGetObservationQuery} from './ObservationApiSlice.jsx';

const EditObservation = () => {
    const {id, reportID} = useParams();
    const {data: Observation, isLoading, isSuccess, isError, error} = useGetObservationQuery(id, {
        pollingInterval: 15000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true,
    });

    const report = Observation.entities[reportID];

    const content = report ? <EditObservationForm report={report} patientID={id}/> :
        <p>Loading...</p>;

    return content;
};

export default EditObservation;
