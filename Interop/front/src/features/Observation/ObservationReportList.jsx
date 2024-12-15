import React, {useState} from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import {useGetObservationQuery} from './ObservationApiSlice.jsx';
import ObservationReport from './ObservationReport.jsx';
import useAuth from '../../hooks/useAuth';
import searchBarTwo from '../../images/searchBarTwo.png';
import CircularLoader from '../../pageLoader/CircularLoader';
import {useSelector} from 'react-redux';
import {selectPatientById} from '../patients/patientsApiSlice';
import '../../css/userList.css';

const ObservationReportList = () => {
    const url = window.location.href;
    const patientID = url.split('/')[5];
    const {isDoctor, isAdmin, isManager} = useAuth();
    const {pathname} = useLocation();
    const navigate = useNavigate();

    // Recherche par mot-clé
    const [q, setQ] = useState('');

    // Récupérer les rapports médicaux pour le patient actuel
    const {data: Observation, isLoading, isSuccess, isError, error} = useGetObservationQuery(patientID, {
        pollingInterval: 15000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true,
    });

    // Récupérer les informations du patient
    const patient = useSelector((state) => selectPatientById(state, patientID));

    let content;

    // Affichage d'un loader si la requête est en cours
    if (isLoading) {
        content = <CircularLoader/>;
    }

    // Affichage d'un message d'erreur si la requête échoue
    if (isError) {
        content = <p className="errmsg">{error?.data?.message ?? 'Failed to load observation reports'}</p>;
    }

    if (isSuccess) {
        const {ids, entities} = Observation;

        // Fonction de recherche
        const searchReports = () => {
            for (let i = 0; i < ids?.length; i++) {
                if (entities[ids[i]].id === Number(q)) {
                    navigate(`/dash/patients/${patientID}/dispositifs/${ids[i]}`);
                }
            }
        };

        // Barre de recherche
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

        // Contenu du tableau de rapports médicaux
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

        content = (
            <>

                {searchBar}

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
            </>
        );
    }

    return (
        <div className="medical-report-list">
            <h2>{patient ? `Observation Reports for ${patient.name}` : 'Observation Reports'}</h2>
            {content}
        </div>
    );
};

export default ObservationReportList;
