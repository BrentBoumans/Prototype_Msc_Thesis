import React, {useState} from "react"

const FillInForm1 = ({transferSingleAnswer_1}) => {

    const [answer, setAnswer] = useState("");

    const handleChange = (e) => {
        setAnswer(e.target.value)
        console.log('from fill in form1', e.target.value)
        transferSingleAnswer_1(e.target.value)
      }

  return (
    <form className='fillInForm'>
        <div className='fillInForm-control'>
            <input type='text' value = {answer} placeholder='type here' onChange={handleChange}/> 
        </div>
    </form>
  )
}

export default FillInForm1


// handleTextChange = async function(event) {

//   await this.setState({text: event.target.value});
//   console.log(this.state.text);
// }