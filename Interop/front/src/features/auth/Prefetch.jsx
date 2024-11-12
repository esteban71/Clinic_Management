import React, {useEffect} from 'react'
import {store} from '../../app/store.jsx'
import {patientsApiSlice} from '../patients/patientsApiSlice.jsx'
import {medecinApiSlice} from '../medecin/medecinApiSlice.jsx'
import {cabinetApiSlice} from '../cabinet/cabinetApiSlice.jsx'
import {receptionistApiSlice} from '../Receptionist/ReceptionistApiSlice.jsx'
import {Outlet} from 'react-router-dom'

import {medicalReportApiSlice} from '../dossierMedical/medicalReportsApiSlice.jsx'

const Prefetch = () => {

    useEffect(() => {
        const patients = store.dispatch(patientsApiSlice.endpoints.getpatients.initiate())
        const medecins = store.dispatch(medecinApiSlice.endpoints.getMedecins.initiate())
        const cabinet = store.dispatch(cabinetApiSlice.endpoints.getCabinets.initiate())
        const receptionists = store.dispatch(receptionistApiSlice.endpoints.getReceptionists.initiate())
        const medicalReports = store.dispatch(medicalReportApiSlice.endpoints.getMedicalReports.initiate())

        return () => {
            patients.unsubscribe()
            medecins.unsubscribe()
            cabinet.unsubscribe()
            receptionists.unsubscribe()
            medicalReports.unsubscribe()
        }
    }, [])

    return <Outlet/>
}

export default Prefetch









