<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Users</h1>
        <hr />
        <br />
        <br />
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" @click="initForm()" v-b-modal.user-modal>Add User</button>
        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Group</th>
              <th scope="col">Role</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.username }}</td>
              <td v-if="user.group !== null">{{ user.group.name }}</td>
              <td v-else></td>
              <td>{{ user.role }}</td>
              <td>
                <button type="button" class="btn btn-warning btn-sm" @click="fillForm(user)" v-b-modal.user-modal>Update</button>
                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteUser(user)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="userModal" id="user-modal" :title="userForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-username-group" label="Username:" label-for="form-username-input">
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="userForm.username"
            required
            placeholder="Enter username"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group" label="Password:" label-for="form-password-input">
          <b-form-input
            id="form-password-input"
            type="password"
            v-model="userForm.password"
            required
            placeholder="Enter password"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-group-group" label="Group:" label-for="form-group-select">
          <b-form-select
            id="form-group-select"
            v-model="userForm.group"
            :options="groupsSelector"
            required
          ></b-form-select>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import Alert from './Alert.vue';
export default {
  components: {
    alert: Alert,
  },
  data() {
    return {
      message: '',
      showMessage: false,
      users: [],
      groups: [],
      groupsSelector: [],
      userForm: {
        userID: null,
        username: "",
        password: "",
        group: null,
        title: "",
        method: ""
      }
    };
  },
  methods: {
    getUsers() {
      const path = "http://localhost:5000/users";
      axios
        .get(path)
        .then(res => {
          this.users = res.data.users;
        })
        .catch(error => {          
          console.error(error);
        });
    },
    getGroups() {
      const path = "http://localhost:5000/groups";
      axios
        .get(path)
        .then(res => {
          this.groups = res.data.groups;
          this.getGroupsSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },
    getGroupsSelector() {        
        this.groupsSelector.push({'value': null, 'text': 'Select'});
        for (let i = 0; i < this.groups.length; i++) {
            let option = {};
            for (let key in this.groups[i]) {                
              if (key == "id") {
                option["value"] = this.groups[i][key];
              } else if (key == "name") {
                option["text"] = this.groups[i][key];
              }
            }            
            this.groupsSelector.push(option);
          }          
    },
    addUser(payload) {
      const path = "http://localhost:5000/users";
      axios
        .post(path, payload)
        .then(res => {
          this.getUsers();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getUsers();
        });
    },
    removeUser(userID) {
      const path = `http://localhost:5000/users/${userID}`;
      axios
        .delete(path)
        .then(res => {
          this.getUsers();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getUsers();
        });
    },
    updateUser(userID, payload) {
      const path = `http://localhost:5000/users/${userID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getUsers();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getUsers();
        });
    },
    onDeleteUser(user){
      this.removeUser(user.id);
    },
    initForm() {
      this.userForm.username = "";
      this.userForm.password = "";
      this.userForm.group = "";
      this.userForm.title = "Add User"
      this.userForm.method = "POST"
    },
    fillForm(user) {
      this.userForm.username = user.username;
      this.userForm.password = user.password;
      this.userForm.group = user.group.id;
      this.userForm.title = "Update User";
      this.userForm.method = "PUT";
      this.userForm.userID = user.id
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();            
      const payload = {
        username: this.userForm.username,
        password: this.userForm.username,
        group_id: this.userForm.group
      };
      if (this.userForm.method == 'POST') {
        this.addUser(payload);
      }
      else if (this.userForm.method == 'PUT') {        
        this.updateUser(this.userForm.userID, payload)
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      this.initForm();
    }
  },
  created() {
    this.getUsers();
    this.getGroups();    
  }
};
</script>