import { chat, infomore } from "../assets";
import styles from "../style";

const Prompts = ({id, title, isActive, onClick}) => {
    
    return(
        <div key={id} className={`${isActive ? "border-main_black" : "border-transparent"} border-[2px] rounded-[13px] border-main_blackflex flex-col 
        items-center my-1.5`} onClick={() => onClick(id)}>
            <div className={`${styles.flexBetween} px-3 py-3.5 cursor-pointer z-[2]`}>
                <img src={chat} alt="chat" className="mr-2 w-[26px]"/>
                <h4 className={`${styles.blackSemibold} text-[18px]  mr-1.5`}>{title}</h4>
                <img src={infomore} alt="" className={`${isActive ? "opacity-1 cursor-pointer" : "opacity-0"} w-[26px] z-[3]`}/>
            </div>
            
        </div>
    )
}

export default Prompts;
