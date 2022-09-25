import unittest
import app
import json


class UnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        self.auth_header = {
            'Authorization': 'Basic ' + "{0}:{1}".format('miguel', 'python')
        }
        self.task = app.Todo

    def tearDown(self):
        pass

    def test_400(self):
        result = self.app.post('/todo/tasks')

        self.assertEqual(result.status_code, 400)
        self.assertIn(b'check', result.data)

    def test_404(self):
        result = self.app.get('/missing-page')

        self.assertEqual(result.status_code, 404)
        self.assertIn(b'not found', result.data)

    def test_405(self):
        result = self.app.post('**')

        self.assertEqual(result.status_code, 405)
        self.assertIn(b'The method is not allowed for the requested URL.', result.data)


    def test_hello_world(self):
        result = self.app.get('/')

        self.assertIn(b'Hello, World!', result.data)

    def test_get_all_tasks(self):
        response = self.app.get('/todo/tasks')

        self.assertIn(b'tasks', response.data)

    def test_get_task(self):
        response = self.app.get('/todo/tasks/1')

        self.assertIn('uri', response.data.decode("UTF-8"))

    def test_get_nonexistent_task(self):
        response = self.app.get('/todo/tasks/-1')

        self.assertIn(b'TODO not found', response.data)

    def test_post_task_400(self):
        data = {"description": "no task name"}
        response = self.app.post('/todo/tasks', headers=self.auth_header, data=json.dumps(data))

        self.assertIn(b'Please check the input format!', response.data)

    def test_post_task_ok(self):
        data = {"name": "Created by unit test", "description": "Auto generated.."}
        response = self.app.post('/todo/tasks', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertIn(b"uri", response.data)

    def test_put_task_ok(self):
        data = {"description": "Updated by unit test"}
        response = self.app.put('/todo/tasks/3', headers=self.auth_header, data=json.dumps(data),
                                content_type='application/json')

        self.assertIn(b"uri", response.data)

    def test_put_task_404(self):
        data = {"description": "Updated by unit test"}
        response = self.app.put('/todo/tasks/0', headers=self.auth_header, data=json.dumps(data),
                                content_type='application/json')

        self.assertIn(b"not found", response.data)

    def test_put_task_400(self):
        response = self.app.put('/todo/tasks/3', headers=self.auth_header, data=None)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please check", response.data)

    def test_put_task_400_not_allowed_status(self):
        data = {"status": "X"}
        response = self.app.put('/todo/tasks/3', headers=self.auth_header, data=json.dumps(data),
                                content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_delete_task_fail(self):
        response = self.app.delete('/todo/tasks/0', headers=self.auth_header,
                                   content_type='application/json')

        self.assertEqual(404, response.status_code)

    # def test_delete_task(self):
    #     # need to input an existed todo_id
    #     task_id =
    #     response = self.app.delete('/todo/tasks/' + str(task_id), headers=self.auth_header,
    #                                content_type='application/json')
    #
    #     self.assertEqual(204, response.status_code)

    def test_filter_by_status(self):
        data = {"status": "D"}
        response = self.app.post('/todo/tasks/filter', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_filter_by_name(self):
        data = {"name": "water"}
        response = self.app.post('/todo/tasks/filter', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_filter_by_name_and_status(self):
        data = {"name": "water", "status": "D"}
        response = self.app.post('/todo/tasks/filter', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_sort_by_due_date(self):
        data = {"due_date": True}
        response = self.app.post('/todo/tasks/sort', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_sort_by_name(self):
        data = {"name": True}
        response = self.app.post('/todo/tasks/sort', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_sort_by_name_and_due_date(self):
        data = {"name": True, "due_date": True}
        response = self.app.post('/todo/tasks/sort', headers=self.auth_header, data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
