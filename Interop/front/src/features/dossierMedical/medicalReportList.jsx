import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useGetMedicalReportsQuery } from './medicalReportsApiSlice';
import MedicalReport from './medicalReport.jsx';
import useAuth from '../../hooks/useAuth';
import searchBarTwo from '../../images/searchBarTwo.png';
import CircularLoader from '../../pageLoader/CircularLoader';
import { useSelector } from 'react-redux';
import { selectPatientById } from '../patients/patientsApiSlice';
import '../../css/userList.css';

const MedicalReportList = () => {
    const url = window.location.href;
    const patientID = url.split('/')[5];
    const { isDoctor, isAdmin, isManager } = useAuth();
    const { pathname } = useLocation();
    const navigate = useNavigate();

    // Recherche par mot-clé
    const [q, setQ] = useState('');

    // Récupérer les rapports médicaux pour le patient actuel
    const { data: medicalReports, isLoading, isSuccess, isError, error } = useGetMedicalReportsQuery(patientID, {
        pollingInterval: 15000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true,
    });

    // Récupérer les informations du patient
    const patient = useSelector((state) => selectPatientById(state, patientID));

    let content;

    // Affichage d'un loader si la requête est en cours
    if (isLoading) {
        content = <CircularLoader />;
    }

    // Affichage d'un message d'erreur si la requête échoue
    if (isError) {
        content = <p className="errmsg">{error?.data?.message ?? 'Failed to load reports'}</p>;
    }

    if (isSuccess) {
        const { ids, entities } = medicalReports;

        // Fonction de recherche
        const searchReports = () => {
            for (let i = 0; i < ids?.length; i++) {
                if (entities[ids[i]].id === Number(q)) {
                    navigate(`/dash/patients/${patientID}/reports/${ids[i]}`);
                }
            }
        };

        // Barre de recherche
        let searchBar;
        if (pathname.includes(`/dash/patients/${patientID}/reports`)) {
            searchBar = (
                <div className="wrapper">
                    <button className="button-search" onClick={searchReports}>
                        <img src={searchBarTwo} alt="search" className="button-search--logo" />
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

        // Fonction pour créer un nouveau rapport
        const handleNewReport = () => {
            navigate(`/dash/patients/${patientID}/reports/new`);
        };

        // Contenu du tableau de rapports médicaux
        const tableContent = ids?.length
            ? ids.map((reportID) => {
                const report = entities[reportID];
                return (
                    <MedicalReport key={reportID} report={report} reportID={reportID} patientID={patientID} />
                );
            })
            : (
                <tr>
                    <td colSpan="6" className="no-reports-message">No reports found.</td>
                </tr>
            );

        content = (
            <>
                {/* Bouton pour ajouter un nouveau rapport médical */}
                <div className="button-wrapper">
                    <button
                        className="button-new-report"
                        onClick={handleNewReport}
                    >
                        New Medical Report
                    </button>
                </div>

                {searchBar}

                <table className="table_patientlist">
                    <thead className="table__thead">
                        <tr className="table_patientlist--header">
                            <th scope="col" className="table__th table__Uppercase">Report ID</th>
                            <th scope="col" className="table__th table__Uppercase">Date</th>
                            <th scope="col" className="table__th table__Uppercase">Title</th>
                            <th scope="col" className="table__th table__Uppercase">Content</th>
                            <th scope="col" className="table__th table__Uppercase">Author</th>
                            <th scope="col" className="table__th table__Uppercase">Edit</th>
                        </tr>
                    </thead>
                    <tbody>{tableContent}</tbody>
                </table>
            </>
        );
    }

    return (
        <div className="medical-report-list">
            <h2>{patient ? `Medical Reports for ${patient.name}` : 'Medical Reports'}</h2>
            {content}
        </div>
    );
};

export default MedicalReportList;
