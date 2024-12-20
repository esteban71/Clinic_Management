import React, {useState} from 'react'
import {useLocation, useNavigate} from 'react-router-dom'
import {useGetpatientsQuery} from './patientsApiSlice.jsx'
import Patient from './Patient'
import useAuth from '../../hooks/useAuth.jsx'
import searchBarTwo from '../../images/searchBarTwo.png'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import '../../css/userList.css'

const PatientsList = () => {

    const {username, isManager, isAdmin, isDoctor, isReceptionist} = useAuth()

    const {pathname} = useLocation()
    const navigate = useNavigate()

    const [q, setQ] = useState('')

    const {
        data: patients,
        isLoading,
        isSuccess,
        isError,
        error
    } = useGetpatientsQuery('patientsList', {
        pollingInterval: 15000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true
    })

    let content

    if (isLoading) {
        content = (
            <CircularLoader/>
        )
    }

    if (isError) {
        content = <p className='errmsg'> {error?.data?.message} </p>
    }

    if (isSuccess) {
        const {ids, entities} = patients


        const searchToken = () => {
            for (let i = 0; i < ids?.length; i++) {
                if (entities[ids[i]].id === Number(q)) {
                    navigate(`/dash/patients/${ids[i]}`)
                }
            }
        }

        let searchBar
        if (pathname === '/dash/patients') {
            searchBar = (
                <div className="wrapper">
                    <button className='button-search' onClick={searchToken}><img src={searchBarTwo} alt="search"
                                                                                 className='button-search--logo'/>
                    </button>
                    <div className="search-wrapper">
                        <label htmlFor="search-form">
                            <input
                                type="search"
                                name="search-form"
                                id="search-form"
                                className="search-input"
                                placeholder="       Enter Patient Token"
                                value={q}
                                /*
                                // set the value of our useState q
                                //  anytime the user types in the search box
                                */
                                onChange={(e) => setQ(e.target.value)}
                            />
                        </label>
                    </div>
                </div>
            )
        }

        let filteredIds = [...ids]
        const tableContent = ids?.length
            ? filteredIds.map(patientID => <Patient key={patientID} patientID={patientID}/>)
            : null
        content = (
            <>
                {searchBar}
                <table className='table_patientlist'>
                    <thead className='table__thead'>
                    <tr className='table_patientlist--header'>
                        <th scope='col' className='table__th table__Uppercase'>Patient Token</th>
                        <th scope='col' className='table__th table__Uppercase'>Patient Name</th>
                        <th scope='col' className='table__th table__Uppercase'>Address</th>
                        <th scope='col' className='table__th table__Uppercase'>Mobile Number</th>
                        {/* <th scope='col' className='table__th table__Uppercase'>Record [One]</th> */}
                        {/* <th scope='col' className='table__th table__Uppercase'>Medicines [One]</th> */}
                        {/* <th scope='col' className='table__th table__Uppercase'>Record [Two]</th> */}
                        {/* <th scope='col' className='table__th table__Uppercase'>Medicines [Two]</th> */}
                        {/* <th scope='col' className='table__th table__Uppercase'>Doctor ID</th> */}
                        {/* <th scope='col' className='table__th table__Uppercase'>View</th> */}
                        <th scope='col' className='table__th table__Uppercase'>View/Edit</th>

                        <th scope='col' className='table__th table__Uppercase'>Medical Report</th>
                        <th scope='col' className='table__th table__Uppercase'>Dispositifs</th>

                    </tr>
                    </thead>

                    <tbody>
                    {tableContent}
                    </tbody>
                </table>
            </>
        )

    }

    return content

}

export default PatientsList

