import dynamic from "next/dynamic";
const ClientOnly = (props) => props.children;
export default dynamic(() => Promise.resolve(ClientOnly), {
    ssr: false,
});
