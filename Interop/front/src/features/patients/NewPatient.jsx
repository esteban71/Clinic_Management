import React from 'react'
import { useSelector } from 'react-redux'
import { selectAllUsers } from '../users/usersApiSlice.jsx'
import NewPatientForm from './NewPatientForm'
import {selectAllMedecins} from "../medecin/medecinApiSlice.jsx";

const NewPatient = () => {
  const medecin = useSelector(selectAllMedecins)

  if(!medecin?.length) return <p>Users not currently available</p>
  
  const content = <NewPatientForm medecin={medecin} />
  
  return content
}

export default NewPatient

