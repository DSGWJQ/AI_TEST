import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/login.vue';
import Register from '../views/Register.vue';
import AiTestCase from '../views/ai_Test_case.vue';
import TestReportBeautifier from '../views/TestReportBeautifier.vue'
import ApiAutoTestRunner from '../views/ApiAutoTestRunner.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/register',
        component: Register
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/ai',
        component: AiTestCase
    },
    {
        path: '/test-report-beautifier',
        component: TestReportBeautifier
    },
    {
        path: '/api-auto-test',
        component: ApiAutoTestRunner
    }
]


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});
export default router;