import React, {useState, useEffect} from "react"
import FillInForm from "./FillInForm"
import FillInForm1 from "./FillInForm1"
import FillInForm2 from "./FillInForm2"
import FillInForm3 from "./FillInForm3"
import FillInForm4 from "./FillInForm4"

const ExBox = ({ exerciseToShow,transferStudentAnswers}) => {

  const [listOfAnswers, setListOfAnswers] = useState(['','','',''])

  function updateListOfAnswers(id,ans) {
    const temp_list = listOfAnswers
    console.log('changing index with number = ' , id )
    temp_list[id] = ans
    console.log('new templist = ', temp_list)
    setListOfAnswers(temp_list)
    transferStudentAnswers(temp_list)
  }

  const [answer1, setAnswer1] = useState("")
  const [answer2, setAnswer2] = useState("")
  const [answer3, setAnswer3] = useState("")
  const [answer4, setAnswer4] = useState("")


  const transferSingleAnswer_1 = (answer1) => {
    console.log('from exbox val 1 = ' , answer1)
    setAnswer1(answer1)
    updateListOfAnswers(0,answer1)
  }

  const transferSingleAnswer_2 = (answer2) => {
    console.log('from exbox val 2 = ' , answer2)
    setAnswer2(answer2)
    updateListOfAnswers(1,answer2)
  }

  const transferSingleAnswer_3 = (answer3) => {
    console.log('from exbox val 3 = ' , answer3)
    setAnswer3(answer3)
    updateListOfAnswers(2,answer3)
  }

  const transferSingleAnswer_4 = (answer4) => {
    console.log('from exbox val 4 = ' , answer4)
    setAnswer4(answer4)
    updateListOfAnswers(3,answer4)
  }


  return (
    <div className = 'exBox'>

      {/* in case exercise is split in 2  */}
      {exerciseToShow.nbOfSkillsTested === 1 &&
         <span key={exerciseToShow.id}>
          {exerciseToShow.exerciseContent_P1} <FillInForm1 transferSingleAnswer_1={transferSingleAnswer_1}/> {exerciseToShow.exerciseContent_P2}
        </span>
      }

       {/* in case exercise is split in 3  */}
       {exerciseToShow.nbOfSkillsTested === 2 &&
         <span key={exerciseToShow.id}>
          {exerciseToShow.exerciseContent_P1} <FillInForm1 transferSingleAnswer_1={transferSingleAnswer_1}/> {exerciseToShow.exerciseContent_P2}
          <FillInForm2 transferSingleAnswer_2={transferSingleAnswer_2}/> {exerciseToShow.exerciseContent_P3}
        </span>
      }

       {/* in case exercise is split in 4  */}
       {exerciseToShow.nbOfSkillsTested === 3 &&
         <span key={exerciseToShow.id}>
          {exerciseToShow.exerciseContent_P1} <FillInForm1 transferSingleAnswer_1={transferSingleAnswer_1}/> {exerciseToShow.exerciseContent_P2}
          <FillInForm2 transferSingleAnswer_2={transferSingleAnswer_2}/> {exerciseToShow.exerciseContent_P3} <FillInForm3 transferSingleAnswer_3={transferSingleAnswer_3}/> 
          {exerciseToShow.exerciseContent_P4} 
        </span>
      }

       {/* in case exercise is split in 5  */}
       {exerciseToShow.nbOfSkillsTested === 4 &&
         <span key={exerciseToShow.id}>
          {exerciseToShow.exerciseContent_P1} <FillInForm1 transferSingleAnswer_1={transferSingleAnswer_1}/> {exerciseToShow.exerciseContent_P2}
          <FillInForm2 transferSingleAnswer_2={transferSingleAnswer_2}/> {exerciseToShow.exerciseContent_P3}<FillInForm3 transferSingleAnswer_3={transferSingleAnswer_3}/> 
          {exerciseToShow.exerciseContent_P4}<FillInForm4 transferSingleAnswer_4={transferSingleAnswer_4}/> {exerciseToShow.exerciseContent_P5}
        </span>
      }

    </div>
  )
}

export default ExBox