import React from 'react'
import { useParams } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectPatientById } from './patientsApiSlice.jsx'
import { selectAllUsers } from '../users/usersApiSlice.jsx'
import EditPatientForm from './EditPatientForm'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import {selectAllMedecins} from "../medecin/medecinApiSlice.jsx";

const EditPatient = () => {

  const { id } = useParams()

  const patient = useSelector(state => selectPatientById(state, id))
  const medecin = useSelector(selectAllMedecins)
  // modify to send all user 

  console.log('users', medecin)

  const content = medecin.length && patient ? <EditPatientForm patient={patient} medecin={medecin} /> : <CircularLoader />

  return content
}

export default EditPatient
