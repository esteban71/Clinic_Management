import React, {useState} from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import {useGetObservationQuery} from './ObservationApiSlice.jsx';
import ObservationReport from './ObservationReport.jsx';
import useAuth from '../../hooks/useAuth';
import searchBarTwo from '../../images/searchBarTwo.png';
import CircularLoader from '../../pageLoader/CircularLoader';
import {useSelector} from 'react-redux';
import {selectPatientById} from '../patients/patientsApiSlice';
import CreateDispositifMedical from '../DispositifMedical/CreateDispositifMedical.jsx';
import {useGetDispositifMedicalQuery} from '../DispositifMedical/DispositifMedicalApiSlice.jsx';
import '../../css/userList.css';
import {MenuItem, Select} from "@mui/material";

const ObservationReportList = () => {
    const url = window.location.href;
    const patientID = url.split('/')[5];
    const {isDoctor, isAdmin, isManager} = useAuth();
    const {pathname} = useLocation();
    const navigate = useNavigate();

    const [q, setQ] = useState('');
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [selectedDevice, setSelectedDevice] = useState(null);

    const {data: Observation, isLoading, isSuccess, isError, error} = useGetObservationQuery(patientID, {
        pollingInterval: 15000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true,
    });


    const {
        data: medicalDevices,
        isLoading: isLoadingDevices,
        isSuccess: isSuccessDevices,
        isError: isErrorDevices,
        error: errorDevices
    } = useGetDispositifMedicalQuery(
        patientID,
        {
            pollingInterval: 15000,
            refetchOnFocus: true,
            refetchOnMountOrArgChange: true,
        }
    );

    const patient = useSelector((state) => selectPatientById(state, patientID));

    let content;

    if (isLoading) {
        content = <CircularLoader/>;
    }

    if (isError) {
        console.log('error:', error?.data);
        if (error?.data?.detail === 'dispositif médical not found') {
            content = <button onClick={() => setShowCreateForm(true)}>Add Medical Device</button>
        } else {
            content = <p className="errmsg">{error?.data?.detail ?? 'Failed to load observation reports'}</p>;
        }
    }

    if (isSuccess && isSuccessDevices) {
        const {ids, entities} = Observation;
        const {ids: deviceIds, entities: deviceEntities} = medicalDevices;

        const searchReports = () => {
            for (let i = 0; i < ids?.length; i++) {
                if (entities[ids[i]].id === Number(q)) {
                    navigate(`/dash/patients/${patientID}/dispositifs/${ids[i]}`);
                }
            }
        };

        let searchBar;
        if (pathname.includes(`/dash/patients/${patientID}/dispositifs`)) {
            searchBar = (
                <div className="wrapper">
                    <button className="button-search" onClick={searchReports}>
                        <img src={searchBarTwo} alt="search" className="button-search--logo"/>
                    </button>
                    <div className="search-wrapper">
                        <label htmlFor="search-form">
                            <input
                                type="search"
                                name="search-form"
                                id="search-form"
                                className="search-input"
                                placeholder="Search Reports"
                                value={q}
                                onChange={(e) => setQ(e.target.value)}
                            />
                        </label>
                    </div>
                </div>
            );
        }

        const tableContent = ids?.length
            ? ids.map((reportID) => {
                const report = entities[reportID];
                return (
                    <ObservationReport key={reportID} report={report} reportID={reportID} patientID={patientID}/>
                );
            })
            : (
                <tr>
                    <td colSpan="6" className="no-reports-message">No observation reports found</td>
                </tr>
            );

        const deviceOptions = deviceIds?.length
            ? deviceIds.map((deviceId) => {
                const device = deviceEntities[deviceId];
                return (
                    <MenuItem key={deviceId} value={deviceId}>
                        {device.name}
                    </MenuItem>
                );
            })
            : <MenuItem value="">No medical devices found</MenuItem>;

        content = (
            <>
                {searchBar}
                {!showCreateForm && (
                    <div className="device-section">
                        <button onClick={() => setShowCreateForm(true)}>Add Medical Device</button>
                        <div className="form__row">
                            <div className="form__divider">
                                <label className="form__label form__checkbox-container" htmlFor="note-username">
                                    Select a Medical Device if you want to modify it:</label>
                                <Select
                                    value={selectedDevice?.id || ''}
                                    onChange={(e) => {
                                        const device = deviceEntities[e.target.value];
                                        setSelectedDevice(device);
                                        setShowCreateForm(true);
                                    }}
                                    displayEmpty
                                    fullWidth
                                    defaultValue=""
                                >
                                    <MenuItem value="" disabled>Select a Medical Device</MenuItem>
                                    {deviceOptions}
                                </Select>
                            </div>
                        </div>
                    </div>
                )}
                {!showCreateForm && (
                    <table className="table_observationlist">
                        <thead className="table__thead">
                        <tr className="table_patientlist--header">
                            <th scope="col" className="table__th table__Uppercase">Report ID</th>
                            <th scope="col" className="table__th table__Uppercase">Date</th>
                            <th scope="col" className="table__th table__Uppercase">Code</th>
                            <th scope="col" className="table__th table__Uppercase">Value</th>
                            <th scope="col" className="table__th table__Uppercase">Unit</th>
                            <th scope="col" className="table__th table__Uppercase">Status</th>
                            <th scope="col" className="table__th table__Uppercase">Component Code</th>
                            <th scope="col" className="table__th table__Uppercase">Component Value</th>
                            <th scope="col" className="table__th table__Uppercase">Component Unit</th>
                            <th scope="col" className="table__th table__Uppercase">View</th>
                        </tr>
                        </thead>
                        <tbody>{tableContent}</tbody>
                    </table>
                )}
            </>
        );
    }

    return (
        <div className="medical-report-list">
            <h2>{patient ? `Observation Reports for ${patient.name}` : 'Observation Reports'}</h2>
            {content}
            {showCreateForm && (
                <div className="create-dispositif-medical-form">
                    <CreateDispositifMedical existingDevice={selectedDevice} patient_id={patientID}
                                             onClose={() => {
                                                 setSelectedDevice(null);
                                                 setShowCreateForm(false);
                                                 window.location.reload();

                                             }}
                    />
                </div>
            )}
        </div>
    );
};

export default ObservationReportList;