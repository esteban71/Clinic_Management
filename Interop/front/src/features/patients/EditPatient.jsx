import React from 'react'
import {useParams} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectPatientById} from './patientsApiSlice.jsx'
import EditPatientForm from './EditPatientForm'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import {selectAllMedecins} from "../medecin/medecinApiSlice.jsx";
import useAuth from "../../hooks/useAuth.jsx";
import {selectAllCabinets} from "../cabinet/cabinetApiSlice.jsx";

const EditPatient = () => {

  const { id } = useParams()

  const patient = useSelector(state => selectPatientById(state, id))
    const {isDoctor} = useAuth()

    const medecin = isDoctor ? [patient.medecin] : useSelector(selectAllMedecins)
    // modify to send all user

    const cabinet_data = useSelector(selectAllCabinets)

    const content = patient ? <EditPatientForm patient={patient} medecin={medecin} cabinet={cabinet_data}/> :
        <CircularLoader/>

  return content
}

export default EditPatient
