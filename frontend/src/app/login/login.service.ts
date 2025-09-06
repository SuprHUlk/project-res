import { User } from "../model/user";
import { post } from "../helpers/axios";

export const signup = async (user: User): Promise<boolean> => {
    try {
        const res = await post("/auth/signup", user);
        return res.isSuccess;
    } catch (e) {
        return false;
    }
};
