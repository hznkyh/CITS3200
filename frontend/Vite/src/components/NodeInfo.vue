<template>
    <p>os type: {{ node.os_type }}</p>
    <p>os version: {{ node.os_version }}</p>
    <p>host ip: {{ node.host_ip }}</p>
    <p>host id: {{ node.host_id }}</p>
    <p>p_u_compromise: {{ node.p_u_compromise }}</p>
    <p>total users: {{ node.total_users }}</p>
    <p>uuid: {{ node.uuid }}</p>
    <p>total services: {{ node.total_services }}</p>
    <p>total nodes: {{ node.total_nodes }}</p>
    <p>compromised: {{ node.compromised }}</p>
    <p>compromised services: {{ node.compromised_services }}</p>
</template>

<script>
export default {
    name: 'NodeInfo',
    props: {
        node: {
            type: Object,
            required: true
        }
    }
}
</script>
