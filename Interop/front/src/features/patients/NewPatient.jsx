import React from 'react'
import {useSelector} from 'react-redux'
import NewPatientForm from './NewPatientForm'
import {selectAllMedecins} from "../medecin/medecinApiSlice.jsx";
import {selectAllCabinets} from "../cabinet/cabinetApiSlice.jsx";

const NewPatient = () => {
  const medecin = useSelector(selectAllMedecins)

  if(!medecin?.length) return <p>Users not currently available</p>

    const cabinet_data = useSelector(selectAllCabinets)

    const content = <NewPatientForm medecin={medecin} cabinet={cabinet_data}/>
  
  return content
}

export default NewPatient

