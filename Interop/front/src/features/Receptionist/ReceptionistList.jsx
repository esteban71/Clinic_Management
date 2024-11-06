import React from 'react'
import useAuth from '../../hooks/useAuth.jsx'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import '../../css/userList.css'
import {useGetReceptionistsQuery} from "./ReceptionistApiSlice.jsx";
import Receptionist from "./Receptionist.jsx";

const ReceptionistList = () => {

    const {isManager, isAdmin, isReceptionist} = useAuth()

    const {
        data: users,
        isLoading,
        isSuccess,
        isError,
        error
    } = useGetReceptionistsQuery('usersList', {
        pollingInterval: 60000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true
    })

    console.log(users)

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
        const {ids, entities} = users

        let entitiesArray = Object.values(entities)

        let tableContent

        if (isManager || isAdmin || isReceptionist) {
            tableContent = ids?.length
                ? ids.map(medecin => <Receptionist key={medecin} ReceptionistID={medecin}/>)
                : null
        }


        content = (
            <table className='table_userlist'>
                <thead className='table__thead'>
                <tr>
                    <th scope='col' className="table__th table__Uppercase">id</th>
                    <th scope='col' className="table__th table__Uppercase">name</th>
                    <th scope='col' className="table__th table__Uppercase">View/Edit</th>
                </tr>
                </thead>

                <tbody>
                {tableContent}
                </tbody>
            </table>
        )
    }

    return content

}

export default ReceptionistList

