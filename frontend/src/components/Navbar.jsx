import { menu, share } from "../assets";
import styles from "../style";

export const Navbar = ({ children }) => {
  if (children === "menu-nav") {
    return (
      <nav className={`${styles.flexBetween} w-full h-[77px] bg-secondary`}>
        <div className="flex items-center ml-6">
          <img src={menu} alt="frameImg" className="w-[27px] object-contain" />
          <h2 className={`${styles.whiteMedium} ml-4 text-[27px] tracking-[1px]`}> Explorer</h2>
        </div>
      </nav>
    );
  } else if(children === "chat-nav") {
    return (
      <nav className={`${styles.flexBetween} w-full h-[77px] bg-secondary border-x-[2px] border-[#485D6A]`}>
        <div className={`${styles.flexBetween} flex-1 px-6`}>
            <h2 className={`${styles.whiteMedium} text-[19px]`}>Abc: Concept & Theory</h2>
            <button className={`${styles.flexCenter} py-3.5 px-3.5 h-[30px] border-[3px] rounded-[20px] border-opacity-20 border-main_black`}>
                <img src={share} alt="share" className="w-[15px] mr-2 object-contain text-white "/>
                <p className={`${styles.whiteNormal} mt-1 text-[12px]`}>Share</p>
            </button>
        </div>
      </nav>
    );
  } else{
    return(
        <nav className={`${styles.flexBetween} w-full h-[77px] bg-secondary`}></nav>
    );
  }
};

export default Navbar;