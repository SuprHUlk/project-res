"use client";
import { useRouter } from "next/navigation";
import { User } from "../model/user";
import { signup } from "./login.service";
import styles from "./page.module.css";
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
    const { login, isAuthenticated, isLoading: authLoading } = useAuth();

    // Redirect to home if already authenticated
    useEffect(() => {
        if (!authLoading && isAuthenticated) {
            router.push("/home");
        }
    }, [isAuthenticated, authLoading, router]);

    // Don't render login form if already authenticated or still checking auth
    if (authLoading || isAuthenticated) {
        return (
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    height: "100vh",
                    fontSize: "18px",
                    color: "#666",
                }}
            >
                Loading...
            </div>
        );
    }

    const handleLogin = async () => {
        setIsLoading(true);
        const user: User = {
            email,
            password,
            isGuestUser: false,
        };

        const res = await signup(user);
        setIsLoading(false);
        if (res) {
            login();
            router.push("/home");
        } else {
            alert("Login failed. Please check your credentials.");
        }
    };

    const handleGuestLogin = async () => {
        setIsLoading(true);
        const user: User = {
            isGuestUser: true,
        };
        const res = await signup(user);
        setIsLoading(false);
        if (res) {
            login();
            router.push("/home");
        } else {
            alert("Guest login failed. Please try again.");
        }
    };

    return (
        <div className={styles.wrapper}>
            <div className={styles.left}>
                <div className={styles.content}>
                    <div className={styles.title}>resume plus plus</div>
                    <div className={styles.desc}>
                        analyze, optimize and enhance
                    </div>
                </div>
                <div className={styles.images}>
                    <div className={styles.img_cont}>
                        <img
                            className={styles.img}
                            src="https://s3.eu-west-2.amazonaws.com/resumedone-eu-west-2-staging/ANViPOwSW-photo.png"
                            alt="login image"
                        />
                    </div>
                    <div
                        className={`${styles.img_cont} ${styles.img_cont_middle}`}
                    >
                        <img
                            className={styles.img}
                            src="https://s3.eu-west-2.amazonaws.com/resumedone-eu-west-2-staging/ANViPOwSW-photo.png"
                            alt="login image"
                        />
                    </div>
                    <div className={styles.img_cont}>
                        <img
                            className={styles.img}
                            src="https://s3.eu-west-2.amazonaws.com/resumedone-eu-west-2-staging/ANViPOwSW-photo.png"
                            alt="login image"
                        />
                    </div>
                </div>
                {/* <div className={`${styles.blob_1} ${styles.blob}`}></div>
        <div className={`${styles.blob_2} ${styles.blob}`}></div> */}
            </div>
            <div className={styles.right}>
                {/* <div className={styles.text}>Login</div> */}
                <form className={styles.form}>
                    <div className={styles.segment}>
                        <h1>sign up</h1>
                    </div>

                    <label className={styles.label}>
                        <input
                            className={styles.input}
                            type="email"
                            placeholder="Email Address"
                            onChange={(e) => {
                                setEmail(e.target.value);
                            }}
                        />
                    </label>
                    <label className={styles.label}>
                        <input
                            className={styles.input}
                            type="password"
                            placeholder="Password"
                            onChange={(e) => {
                                setPassword(e.target.value);
                            }}
                        />
                    </label>
                    <button
                        className={`${styles.button} ${styles.buttonRed}`}
                        type="button"
                        onClick={handleLogin}
                        disabled={isLoading}
                    >
                        <i className="icon ion-md-lock"></i>
                        {isLoading ? "Signing in..." : "plus plus"}
                    </button>
                    <p>not sure?</p>
                    <button
                        className={`${styles.button} ${styles.buttonRed}`}
                        type="button"
                        onClick={handleGuestLogin}
                        disabled={isLoading}
                    >
                        <i className="icon ion-md-lock"></i>
                        {isLoading ? "Signing in..." : "guest login"}
                    </button>
                    {/*                     
                    <div className={styles.segment}>
                        <button className={`${styles.button} ${styles.buttonUnit}`} type="button"><i className="icon ion-md-arrow-back"></i></button>
                        <button className={`${styles.button} ${styles.buttonUnit}`} type="button"><i className="icon ion-md-bookmark"></i></button>
                        <button className={`${styles.button} ${styles.buttonUnit}`} type="button"><i className="icon ion-md-settings"></i></button>
                    </div> */}

                    {/* <div className={styles.inputGroup}>
                        <label className={styles.label}>
                        <input className={styles.input} type="text" placeholder="Email Address"/>
                        </label>
                        <button className={`${styles.button} ${styles.buttonUnit}`} type="button"><i className="icon ion-md-search"></i></button>
                    </div>
                     */}
                </form>
            </div>
        </div>
    );
}
