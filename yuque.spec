module Yuque {

  prop basePath = "/api/v2";

  type @domain = string
  type @authToken = string

  type @toJSON = (object): string
  type @readJSON = async ($Response): object

  model Config {
    authToken: string,
    domain: string
  }

  init(config: Config);

  api get(path: string, params: object): object {
    protocol = 'https';
    method = 'GET';
    pathname = `${__module.basePath}${path}`;
    query = {
      ...params
    };
    headers = {
      host = @domain,
      x-auth-token = @authToken,
      user-agent = "tea/nodejs",
    };
  } returns {
    var result = @readJSON(__response);
    return result;
  }

  api post(path: string, data: object): object {
    method = 'POST';
    pathname = `${__module.basePath}${path}`;
    headers = {
      host = @domain,
      x-auth-token = @authToken,
      user-agent = "tea/nodejs"
    };
    body = @toJSON(data);
  } returns {
    var result = @readJSON(__response);
    return result;
  }

  api put(path: string, data: object): object {
    method = 'PUT';
    pathname = `${__module.basePath}${path}`;
    headers = {
      host = @domain,
      x-auth-token = @authToken,
      user-agent = "tea/nodejs"
    };
    body = @toJSON(data);
  } returns {
    var result = @readJSON(__response);
    return result;
  }

  api destroy(path: string, data: object): object {
    method = 'DELETE';
    pathname = `${__module.basePath}${path}`;
    headers = {
      host = @domain,
      x-auth-token = @authToken,
      user-agent = "tea/nodejs"
    };
    body = @toJSON(data);
  } returns {
    var result = @readJSON(__response);
    return result;
  }

  model Response<T> = {
    data: T
  };

  model Hello = {
    message: string
  };

  async function hello(): Response<Hello> {
    return get('/hello', {});
  }

  // model Document = {
  //   id: number,
  //   title: string,
  //   slug: string,
  //   body: string,
  //   likes_count: number,
  //   created_at: string,
  //   updated_at: string,
  // }

  // function createDocument(repoid: string, doc: Document): Document {
  //  return post<Document>(`/repos/${repoid}/docs`, doc);
  // }

  model User = {
    id: number(description="用户编号"),
    type: string(description="类型 [User - 用户, Group - 团队]"),
    login: string(description="用户个人路径"),
    name: string(description="昵称"),
    description: string(description="描述"),
    avatar_url: string(description="头像 URL"),
    created_at: string(description="创建时间"),
    updated_at: string(description="更新时间")
  }

  /**
   * 获取单个用户信息
   * @param login 用户个人路径
   */
  async function getUserById(login: string): Response<User> {
    return get(`/users/${login}`, {});
  }

  /**
   * 获取认证的用户的个人信息
   */
  async function getUser(): Response<User> {
    return get(`/user`, {});
  }

  model Group = {
    id?: string,
    login: string,
    name: string,
    avatar_url?: string,
    owner_id: string,
    description: string,
    created_at?: string,
    updated_at?: string,
  }

  /**
   * 获取某个用户的加入的组织列表
   * @param login 用户个人路径
   */
  async function getGroupsByUser(login: string): Response<[Group]> {
    return get(`/users/${login}/groups`, {});
  }

  /**
   * 获取公开组织列表
   */
  async function getGroups(): Response<[User]> {
    return get(`/groups`, {});
  }

  /**
   * 创建 Group
   */
  async function createGroup(group: Group): Response<Group> {
    return post(`/groups`, group);
  }

  model GroupDetailResponse = {
    abilities: {
      read: boolean,
      update: boolean,
      destroy: boolean,
      group_user: {
        create: boolean,
        update: boolean,
        destroy: boolean
      },
      repo: {
        create: boolean,
        update: boolean,
        destroy: boolean
      }
    },
    data: [ Group ]
  }

  /**
   * 获取公开组织列表
   */
  async function getGroup(groupid: string): GroupDetailResponse {
    return get(`/groups/${groupid}`, {});
  }

  /**
   * 更新团队信息
   */
  async function updateGroup(groupid: string, params: object): Response<Group> {
    return put(`/groups/${groupid}`, params);
  }

  /**
   * 删除团队
   */
  async function destryGroup(groupid: string): object {
    return destroy(`/groups/${groupid}`, {});
  }

  model GroupUser = {
    id: number(description="成员编号"),
    group_id: number(description="团队 id"),
    user_id: number(description="成员 id"),
    role: number(description="角色，0 为管理员，1 为成员"),
    user: User(description="用户详细信息"),
    created_at: string(description="创建时间"),
    updated_at: string(description="更新时间")
  }

  /**
   * 获取组织成员信息
   */
  async function getGroupMembers(groupid: string): Response<[GroupUser]> {
    return get(`/groups/${groupid}/users`, {});
  }

  /**
   * 更新或创建团队成员
   */
  async function updateGroupMember(groupid: string, userid: string, params: object): Response<GroupUser> {
    return put(`/groups/${groupid}/users/${userid}`, params);
  }

  /**
   * 删除团队成员
   */
  async function destroyGroupMember(groupid: string, userid: string): object {
    return destroy(`/groups/${groupid}/users/${userid}`, {});
  }

  model Book = {
    id: number(description="仓库编号"),
    type: string(description="类型 [Book - 文档]"),
    slug: string(description="仓库路径"),
    name: string(description="名称"),
    namespace: string(description="仓库完整路径 user.login/book.slug"),
    user_id: number(description="所属的团队/用户编号"),
    user: User(description="<UserSerializer>"),
    description: string(description="介绍"),
    creator_id: number(description="创建人 User Id"),
    public: number(description="公开状态 [1 - 公开, 0 - 私密]"),
    likes_count: number(description="喜欢数量"),
    watches_count: number(description="订阅数量"),
    created_at: string(description="创建时间"),
    updated_at: string(description="更新时间")
  }

  /**
   * 获取一个用户/团队下的知识库
   */
  async function getBooksByUser(userid: string, params: object): Response<[Book]> {
    return get(`/users/${userid}/repos`, params);
  }

  /**
   * 在用户/团队下创建知识库
   */
  async function createBook(userid: string, params: object): Response<[Book]> {
    return post(`/groups/${userid}/repos`, params);
  }

  /**
   * 获取一个知识库详情
   */
  async function getBook(namespace: string): Response<Book> {
    return get(`/repos/${namespace}`, {});
  }

  /**
   * 更新知识库
   */
  async function updateBook(namespace: string, params: object): Response<Book> {
    return put(`/repos/${namespace}`, params);
  }

  /**
   * 删除知识库
   */
  async function destroyBook(namespace: string): object {
    return destroy(`/repos/${namespace}`, {});
  }

  model BookToc = {
    title: string(description="标题"),
    slug: string(description="路径"),
    depth: number(description="层级"),
  }

  /**
   * 获取一个知识库的目录
   */
  async function getBookToc(namespace: string): Response<[BookToc]> {
    return get(`/repos/${namespace}/toc`, {});
  }

  model SearchQuery = {
    query: string,
    type?: string
  }

  /**
   * FIXME: 如何传递 query
   * 搜索知识库
   */
  async function searchBook(params: SearchQuery): Response<[Book]> {
    return get(`/search/repos`, params);
  }

  model Doc {
    id: number(description="文档编号"),
    slug: string(description="文档路径"),
    title: string(description="标题"),
    book_id: number(description="仓库编号，就是 repo_id"),
    book: Book(description="仓库信息 <BookSerializer>，就是 repo 信息"),
    user_id: number(description="用户/团队编号"),
    user: User(description="用户/团队信息 <UserSerializer>"),
    format: string(description="描述了正文的格式 [lake , markdown]"),
    body: string(description="正文 Markdown 源代码"),
    body_draft: string(description="草稿 Markdown 源代码"),
    body_html: string(description="转换过后的正文 HTML"),
    body_lake: string(description="语雀 lake 格式的文档内容"),
    creator_id: number(description="文档创建人 User Id"),
    public: number(description="公开级别 [0 - 私密, 1 - 公开]"),
    status: number(description="状态 [0 - 草稿, 1 - 发布]"),
    likes_count: number(description="赞数量"),
    comments_count: number(description="评论数量"),
    content_updated_at: string(description="文档内容更新时间"),
    deleted_at: string(description="删除时间，未删除为 null"),
    created_at: string(description="创建时间"),
    updated_at: string(description="更新时间"),
  }

  /**
   * 获取知识库下文档列表
   */
  async function getDocs(namespace: string): Response<[Doc]> {
    return get(`/repos/${namespace}/docs`, {});
  }

  /**
   * 获取单篇文档详情
   */
  async function getDoc(namespace: string, slug: string): Response<Doc> {
    return get(`/repos/${namespace}/docs/${slug}`, {});
  }

  /**
   * 创建文档
   */
  async function createDoc(namespace: string, params: object): Response<Doc> {
    return post(`/repos/${namespace}/docs`, params);
  }

  /**
   * 更新文档
   */
  async function updateDoc(namespace: string, slug: string, params: object): Response<Doc> {
    return put(`/repos/${namespace}/docs/${slug}`, params);
  }

  /**
   * 删除文档
   */
  async function destroyDoc(namespace: string, slug: string): object {
    return destroy(`/repos/${namespace}/docs/${slug}`, {});
  }
}
